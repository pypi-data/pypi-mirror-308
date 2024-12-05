# Copyright (c) 2024 Roboto Technologies, Inc.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import enum
import typing

import pydantic

from ...pydantic import (
    validate_nonzero_gitpath_specs,
)
from ...query import ConditionType
from .action_record import (
    ActionReference,
    ComputeRequirements,
    ContainerParameters,
)
from .invocation_record import (
    InvocationDataSource,
)


class TriggerForEachPrimitive(str, enum.Enum):
    """
    Trigger for each enum.
    """

    Dataset = "dataset"
    DatasetFile = "dataset_file"


class TriggerRecord(pydantic.BaseModel):
    """
    A wire-transmissible representation of an trigger.
    """

    trigger_id: str
    name: str
    org_id: str
    created: datetime.datetime
    created_by: str
    modified: datetime.datetime
    modified_by: str
    action: ActionReference
    required_inputs: list[str]
    service_user_id: str
    for_each: TriggerForEachPrimitive = TriggerForEachPrimitive.Dataset
    enabled: bool = True
    parameter_values: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    additional_inputs: typing.Optional[list[str]] = None
    compute_requirement_overrides: typing.Optional[ComputeRequirements] = None
    container_parameter_overrides: typing.Optional[ContainerParameters] = None
    condition: typing.Optional[ConditionType] = None
    timeout: typing.Optional[int] = None

    @pydantic.field_validator("required_inputs")
    def validate_required_inputs(cls, value: list[str]) -> list[str]:
        return validate_nonzero_gitpath_specs(value)

    @pydantic.field_validator("additional_inputs")
    def validate_additional_inputs(
        cls, value: typing.Optional[list[str]]
    ) -> typing.Optional[list[str]]:
        if value is None or len(value) == 0:
            return []

        return validate_nonzero_gitpath_specs(value)


class TriggerEvaluationCause(enum.Enum):
    """
    The cause of a TriggerEvaluationRecord is the reason why the trigger was selected for evaluation.
    """

    DatasetMetadataUpdate = "dataset_metadata_update"
    FileUpload = "file_upload"


class TriggerEvaluationStatus(enum.Enum):
    """
    When a trigger is selected for evaluation,
    a trigger evaluation record is created with a status of Pending.
    The evaluation can either run to completion (regardless of its outcome),
    in which case the status is Evaluated, or hit an unexpected exception,
    in which case the status is Failed.
    """

    Pending = "pending"
    Evaluated = "evaluated"
    Failed = "failed"


class TriggerEvaluationOutcome(enum.Enum):
    """
    The outcome of a TriggerEvaluationRecord is the result of the evaluation.
    A trigger can either invoke its associated action (one or many times) or be skipped.
    If skipped, a skip reason is provided.
    """

    InvokedAction = "invoked_action"
    Skipped = "skipped"


class TriggerEvaluationOutcomeReason(enum.Enum):
    """Context for why a trigger evaluation has its TriggerEvaluationOutcome"""

    AlreadyRun = "already_run"
    """
    This trigger has already run its associated action for this dataset and/or file.
    """

    ConditionNotMet = "condition_not_met"
    """
    The trigger's condition is not met.
    """

    NoMatchingFiles = "no_matching_files"
    """
    In the case of a dataset trigger,
    there is no subset of files that, combined, match ALL of the trigger's required inputs.

    In the case of a file trigger,
    there are no files that match ANY of the trigger's required inputs.
    """

    TriggerDisabled = "trigger_disabled"
    """
    The trigger is disabled.
    """


class TriggerEvaluationRecord(pydantic.BaseModel):
    """
    Record of a point-in-time evaluation of whether to invoke an action associated with a trigger for a data source.
    """

    trigger_evaluation_id: int  # Auto-generated by the database
    trigger_id: str
    data_source: InvocationDataSource
    evaluation_start: datetime.datetime
    evaluation_end: typing.Optional[datetime.datetime] = None
    status: TriggerEvaluationStatus
    status_detail: typing.Optional[str] = (
        None  # E.g., exception that caused the evaluation to fail
    )
    outcome: typing.Optional[TriggerEvaluationOutcome] = None
    outcome_reason: typing.Optional[TriggerEvaluationOutcomeReason] = None
    cause: typing.Optional[TriggerEvaluationCause] = None
