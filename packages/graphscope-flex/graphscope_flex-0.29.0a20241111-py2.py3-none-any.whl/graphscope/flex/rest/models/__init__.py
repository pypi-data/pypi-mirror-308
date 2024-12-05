# coding: utf-8

# flake8: noqa
"""
    GraphScope FLEX HTTP SERVICE API

    This is a specification for GraphScope FLEX HTTP service based on the OpenAPI 3.0 specification. You can find out more details about specification at [doc](https://swagger.io/specification/v3/).

    The version of the OpenAPI document: 1.0.0
    Contact: graphscope@alibaba-inc.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


# import models into model package
from graphscope.flex.rest.models.base_edge_type import BaseEdgeType
from graphscope.flex.rest.models.base_edge_type_vertex_type_pair_relations_inner import BaseEdgeTypeVertexTypePairRelationsInner
from graphscope.flex.rest.models.base_edge_type_vertex_type_pair_relations_inner_x_csr_params import BaseEdgeTypeVertexTypePairRelationsInnerXCsrParams
from graphscope.flex.rest.models.base_property_meta import BasePropertyMeta
from graphscope.flex.rest.models.base_vertex_type import BaseVertexType
from graphscope.flex.rest.models.base_vertex_type_x_csr_params import BaseVertexTypeXCsrParams
from graphscope.flex.rest.models.column_mapping import ColumnMapping
from graphscope.flex.rest.models.column_mapping_column import ColumnMappingColumn
from graphscope.flex.rest.models.create_alert_receiver_request import CreateAlertReceiverRequest
from graphscope.flex.rest.models.create_alert_rule_request import CreateAlertRuleRequest
from graphscope.flex.rest.models.create_dataloading_job_response import CreateDataloadingJobResponse
from graphscope.flex.rest.models.create_edge_type import CreateEdgeType
from graphscope.flex.rest.models.create_graph_request import CreateGraphRequest
from graphscope.flex.rest.models.create_graph_response import CreateGraphResponse
from graphscope.flex.rest.models.create_graph_schema_request import CreateGraphSchemaRequest
from graphscope.flex.rest.models.create_property_meta import CreatePropertyMeta
from graphscope.flex.rest.models.create_stored_proc_request import CreateStoredProcRequest
from graphscope.flex.rest.models.create_stored_proc_response import CreateStoredProcResponse
from graphscope.flex.rest.models.create_vertex_type import CreateVertexType
from graphscope.flex.rest.models.dataloading_job_config import DataloadingJobConfig
from graphscope.flex.rest.models.dataloading_job_config_edges_inner import DataloadingJobConfigEdgesInner
from graphscope.flex.rest.models.dataloading_job_config_loading_config import DataloadingJobConfigLoadingConfig
from graphscope.flex.rest.models.dataloading_job_config_loading_config_format import DataloadingJobConfigLoadingConfigFormat
from graphscope.flex.rest.models.dataloading_job_config_vertices_inner import DataloadingJobConfigVerticesInner
from graphscope.flex.rest.models.dataloading_mr_job_config import DataloadingMRJobConfig
from graphscope.flex.rest.models.date_type import DateType
from graphscope.flex.rest.models.edge_mapping import EdgeMapping
from graphscope.flex.rest.models.edge_mapping_type_triplet import EdgeMappingTypeTriplet
from graphscope.flex.rest.models.error import Error
from graphscope.flex.rest.models.gs_data_type import GSDataType
from graphscope.flex.rest.models.get_alert_message_response import GetAlertMessageResponse
from graphscope.flex.rest.models.get_alert_receiver_response import GetAlertReceiverResponse
from graphscope.flex.rest.models.get_alert_rule_response import GetAlertRuleResponse
from graphscope.flex.rest.models.get_edge_type import GetEdgeType
from graphscope.flex.rest.models.get_graph_response import GetGraphResponse
from graphscope.flex.rest.models.get_graph_schema_response import GetGraphSchemaResponse
from graphscope.flex.rest.models.get_pod_log_response import GetPodLogResponse
from graphscope.flex.rest.models.get_property_meta import GetPropertyMeta
from graphscope.flex.rest.models.get_resource_usage_response import GetResourceUsageResponse
from graphscope.flex.rest.models.get_storage_usage_response import GetStorageUsageResponse
from graphscope.flex.rest.models.get_stored_proc_response import GetStoredProcResponse
from graphscope.flex.rest.models.get_vertex_type import GetVertexType
from graphscope.flex.rest.models.job_status import JobStatus
from graphscope.flex.rest.models.long_text import LongText
from graphscope.flex.rest.models.node_status import NodeStatus
from graphscope.flex.rest.models.parameter import Parameter
from graphscope.flex.rest.models.pod_status import PodStatus
from graphscope.flex.rest.models.primitive_type import PrimitiveType
from graphscope.flex.rest.models.resource_usage import ResourceUsage
from graphscope.flex.rest.models.running_deployment_info import RunningDeploymentInfo
from graphscope.flex.rest.models.running_deployment_status import RunningDeploymentStatus
from graphscope.flex.rest.models.schema_mapping import SchemaMapping
from graphscope.flex.rest.models.service_status import ServiceStatus
from graphscope.flex.rest.models.service_status_sdk_endpoints import ServiceStatusSdkEndpoints
from graphscope.flex.rest.models.start_service_request import StartServiceRequest
from graphscope.flex.rest.models.stored_procedure_meta import StoredProcedureMeta
from graphscope.flex.rest.models.string_type import StringType
from graphscope.flex.rest.models.string_type_string import StringTypeString
from graphscope.flex.rest.models.temporal_type import TemporalType
from graphscope.flex.rest.models.temporal_type_temporal import TemporalTypeTemporal
from graphscope.flex.rest.models.time_stamp_type import TimeStampType
from graphscope.flex.rest.models.update_alert_message_status_request import UpdateAlertMessageStatusRequest
from graphscope.flex.rest.models.update_stored_proc_request import UpdateStoredProcRequest
from graphscope.flex.rest.models.upload_file_response import UploadFileResponse
from graphscope.flex.rest.models.vertex_mapping import VertexMapping
