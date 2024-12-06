from __future__ import annotations

import dataclasses
from typing import cast

from blueapi.core import BlueskyContext, MsgGenerator
from dodal.devices.aperturescatterguard import ApertureScatterguard
from dodal.devices.attenuator import Attenuator
from dodal.devices.backlight import Backlight
from dodal.devices.dcm import DCM
from dodal.devices.detector.detector_motion import DetectorMotion
from dodal.devices.eiger import EigerDetector
from dodal.devices.fast_grid_scan import PandAFastGridScan, ZebraFastGridScan
from dodal.devices.flux import Flux
from dodal.devices.focusing_mirror import FocusingMirrorWithStripes, MirrorVoltages
from dodal.devices.motors import XYZPositioner
from dodal.devices.oav.oav_detector import OAV
from dodal.devices.oav.pin_image_recognition import PinTipDetection
from dodal.devices.robot import BartRobot, SampleLocation
from dodal.devices.s4_slit_gaps import S4SlitGaps
from dodal.devices.smargon import Smargon
from dodal.devices.synchrotron import Synchrotron
from dodal.devices.thawer import Thawer
from dodal.devices.undulator import Undulator
from dodal.devices.undulator_dcm import UndulatorDCM
from dodal.devices.webcam import Webcam
from dodal.devices.xbpm_feedback import XBPMFeedback
from dodal.devices.zebra import Zebra
from dodal.devices.zebra_controlled_shutter import ZebraShutter
from dodal.devices.zocalo import ZocaloResults
from dodal.log import LOGGER
from ophyd_async.fastcs.panda import HDFPanda

from mx_bluesky.common.parameters.constants import OavConstants
from mx_bluesky.hyperion.device_setup_plans.utils import (
    fill_in_energy_if_not_supplied,
    start_preparing_data_collection_then_do_plan,
)
from mx_bluesky.hyperion.experiment_plans.grid_detect_then_xray_centre_plan import (
    GridDetectThenXRayCentreComposite,
)
from mx_bluesky.hyperion.experiment_plans.pin_centre_then_xray_centre_plan import (
    pin_centre_then_xray_centre_plan,
)
from mx_bluesky.hyperion.experiment_plans.robot_load_and_change_energy import (
    RobotLoadAndEnergyChangeComposite,
    pin_already_loaded,
    robot_load_and_change_energy_plan,
)
from mx_bluesky.hyperion.parameters.constants import CONST
from mx_bluesky.hyperion.parameters.gridscan import RobotLoadThenCentre


@dataclasses.dataclass
class RobotLoadThenCentreComposite:
    # common fields
    xbpm_feedback: XBPMFeedback
    attenuator: Attenuator

    # GridDetectThenXRayCentreComposite fields
    aperture_scatterguard: ApertureScatterguard
    backlight: Backlight
    detector_motion: DetectorMotion
    eiger: EigerDetector
    zebra_fast_grid_scan: ZebraFastGridScan
    flux: Flux
    oav: OAV
    pin_tip_detection: PinTipDetection
    smargon: Smargon
    synchrotron: Synchrotron
    s4_slit_gaps: S4SlitGaps
    undulator: Undulator
    zebra: Zebra
    zocalo: ZocaloResults
    panda: HDFPanda
    panda_fast_grid_scan: PandAFastGridScan
    thawer: Thawer
    sample_shutter: ZebraShutter

    # SetEnergyComposite fields
    vfm: FocusingMirrorWithStripes
    mirror_voltages: MirrorVoltages
    dcm: DCM
    undulator_dcm: UndulatorDCM

    # RobotLoad fields
    robot: BartRobot
    webcam: Webcam
    lower_gonio: XYZPositioner


def create_devices(context: BlueskyContext) -> RobotLoadThenCentreComposite:
    from mx_bluesky.hyperion.utils.context import device_composite_from_context

    return device_composite_from_context(context, RobotLoadThenCentreComposite)


def centring_plan_from_robot_load_params(
    composite: RobotLoadThenCentreComposite,
    params: RobotLoadThenCentre,
    oav_config_file: str = OavConstants.OAV_CONFIG_JSON,
):
    yield from pin_centre_then_xray_centre_plan(
        cast(GridDetectThenXRayCentreComposite, composite),
        params.pin_centre_then_xray_centre_params(),
    )


def robot_load_then_centre_plan(
    composite: RobotLoadThenCentreComposite,
    params: RobotLoadThenCentre,
    oav_config_file: str = OavConstants.OAV_CONFIG_JSON,
):
    yield from robot_load_and_change_energy_plan(
        cast(RobotLoadAndEnergyChangeComposite, composite),
        params.robot_load_params(),
    )

    yield from centring_plan_from_robot_load_params(composite, params, oav_config_file)


def robot_load_then_centre(
    composite: RobotLoadThenCentreComposite,
    parameters: RobotLoadThenCentre,
) -> MsgGenerator:
    eiger: EigerDetector = composite.eiger

    # TODO: get these from one source of truth #254
    assert parameters.sample_puck is not None
    assert parameters.sample_pin is not None

    sample_location = SampleLocation(parameters.sample_puck, parameters.sample_pin)

    doing_sample_load = not (
        yield from pin_already_loaded(composite.robot, sample_location)
    )

    doing_chi_change = parameters.chi_start_deg is not None

    if doing_sample_load:
        plan = robot_load_then_centre_plan(
            composite,
            parameters,
        )
        LOGGER.info("Pin not loaded, loading and centring")
    elif doing_chi_change:
        plan = centring_plan_from_robot_load_params(composite, parameters)
        LOGGER.info("Pin already loaded but chi changed so centring")
    else:
        LOGGER.info("Pin already loaded and chi not changed so doing nothing")
        return

    detector_params = yield from fill_in_energy_if_not_supplied(
        composite.dcm, parameters.detector_params
    )

    eiger.set_detector_parameters(detector_params)

    yield from start_preparing_data_collection_then_do_plan(
        eiger,
        composite.detector_motion,
        parameters.detector_distance_mm,
        plan,
        group=CONST.WAIT.GRID_READY_FOR_DC,
    )
