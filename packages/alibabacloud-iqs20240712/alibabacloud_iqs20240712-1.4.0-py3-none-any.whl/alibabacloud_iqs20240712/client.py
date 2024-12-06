# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_iqs20240712 import models as iqs20240712_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('iqs', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def bicycling_direction_with_options(
        self,
        request: iqs20240712_models.BicyclingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.BicyclingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: BicyclingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BicyclingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/bicycling',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.BicyclingDirectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def bicycling_direction_with_options_async(
        self,
        request: iqs20240712_models.BicyclingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.BicyclingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: BicyclingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BicyclingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/bicycling',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.BicyclingDirectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def bicycling_direction(
        self,
        request: iqs20240712_models.BicyclingDirectionRequest,
    ) -> iqs20240712_models.BicyclingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionRequest
        @return: BicyclingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.bicycling_direction_with_options(request, headers, runtime)

    async def bicycling_direction_async(
        self,
        request: iqs20240712_models.BicyclingDirectionRequest,
    ) -> iqs20240712_models.BicyclingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionRequest
        @return: BicyclingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.bicycling_direction_with_options_async(request, headers, runtime)

    def bicycling_direction_nova_with_options(
        self,
        request: iqs20240712_models.BicyclingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.BicyclingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: BicyclingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BicyclingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/bicycling',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.BicyclingDirectionNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def bicycling_direction_nova_with_options_async(
        self,
        request: iqs20240712_models.BicyclingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.BicyclingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: BicyclingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BicyclingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/bicycling',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.BicyclingDirectionNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def bicycling_direction_nova(
        self,
        request: iqs20240712_models.BicyclingDirectionNovaRequest,
    ) -> iqs20240712_models.BicyclingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionNovaRequest
        @return: BicyclingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.bicycling_direction_nova_with_options(request, headers, runtime)

    async def bicycling_direction_nova_async(
        self,
        request: iqs20240712_models.BicyclingDirectionNovaRequest,
    ) -> iqs20240712_models.BicyclingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的骑行路线规划方案
        
        @param request: BicyclingDirectionNovaRequest
        @return: BicyclingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.bicycling_direction_nova_with_options_async(request, headers, runtime)

    def circle_traffic_status_with_options(
        self,
        request: iqs20240712_models.CircleTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.CircleTrafficStatusResponse:
        """
        @summary 实时查询圆形区域内的交通信息查询
        
        @param request: CircleTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CircleTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CircleTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/circle',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.CircleTrafficStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def circle_traffic_status_with_options_async(
        self,
        request: iqs20240712_models.CircleTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.CircleTrafficStatusResponse:
        """
        @summary 实时查询圆形区域内的交通信息查询
        
        @param request: CircleTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CircleTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CircleTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/circle',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.CircleTrafficStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def circle_traffic_status(
        self,
        request: iqs20240712_models.CircleTrafficStatusRequest,
    ) -> iqs20240712_models.CircleTrafficStatusResponse:
        """
        @summary 实时查询圆形区域内的交通信息查询
        
        @param request: CircleTrafficStatusRequest
        @return: CircleTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.circle_traffic_status_with_options(request, headers, runtime)

    async def circle_traffic_status_async(
        self,
        request: iqs20240712_models.CircleTrafficStatusRequest,
    ) -> iqs20240712_models.CircleTrafficStatusResponse:
        """
        @summary 实时查询圆形区域内的交通信息查询
        
        @param request: CircleTrafficStatusRequest
        @return: CircleTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.circle_traffic_status_with_options_async(request, headers, runtime)

    def common_query_by_scene_with_options(
        self,
        request: iqs20240712_models.CommonQueryBySceneRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.CommonQueryBySceneResponse:
        """
        @summary 自然语言通用查询
        
        @param request: CommonQueryBySceneRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonQueryBySceneResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='CommonQueryByScene',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v2/nl/common',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.CommonQueryBySceneResponse(),
            self.call_api(params, req, runtime)
        )

    async def common_query_by_scene_with_options_async(
        self,
        request: iqs20240712_models.CommonQueryBySceneRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.CommonQueryBySceneResponse:
        """
        @summary 自然语言通用查询
        
        @param request: CommonQueryBySceneRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonQueryBySceneResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='CommonQueryByScene',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v2/nl/common',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.CommonQueryBySceneResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def common_query_by_scene(
        self,
        request: iqs20240712_models.CommonQueryBySceneRequest,
    ) -> iqs20240712_models.CommonQueryBySceneResponse:
        """
        @summary 自然语言通用查询
        
        @param request: CommonQueryBySceneRequest
        @return: CommonQueryBySceneResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.common_query_by_scene_with_options(request, headers, runtime)

    async def common_query_by_scene_async(
        self,
        request: iqs20240712_models.CommonQueryBySceneRequest,
    ) -> iqs20240712_models.CommonQueryBySceneResponse:
        """
        @summary 自然语言通用查询
        
        @param request: CommonQueryBySceneRequest
        @return: CommonQueryBySceneResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.common_query_by_scene_with_options_async(request, headers, runtime)

    def driving_direction_with_options(
        self,
        request: iqs20240712_models.DrivingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.DrivingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DrivingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DrivingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/driving',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.DrivingDirectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def driving_direction_with_options_async(
        self,
        request: iqs20240712_models.DrivingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.DrivingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DrivingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DrivingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/driving',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.DrivingDirectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def driving_direction(
        self,
        request: iqs20240712_models.DrivingDirectionRequest,
    ) -> iqs20240712_models.DrivingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionRequest
        @return: DrivingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.driving_direction_with_options(request, headers, runtime)

    async def driving_direction_async(
        self,
        request: iqs20240712_models.DrivingDirectionRequest,
    ) -> iqs20240712_models.DrivingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionRequest
        @return: DrivingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.driving_direction_with_options_async(request, headers, runtime)

    def driving_direction_nova_with_options(
        self,
        request: iqs20240712_models.DrivingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.DrivingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DrivingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.car_type):
            query['carType'] = request.car_type
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        if not UtilClient.is_unset(request.plate):
            query['plate'] = request.plate
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DrivingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/driving',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.DrivingDirectionNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def driving_direction_nova_with_options_async(
        self,
        request: iqs20240712_models.DrivingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.DrivingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: DrivingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.car_type):
            query['carType'] = request.car_type
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        if not UtilClient.is_unset(request.plate):
            query['plate'] = request.plate
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DrivingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/driving',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.DrivingDirectionNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def driving_direction_nova(
        self,
        request: iqs20240712_models.DrivingDirectionNovaRequest,
    ) -> iqs20240712_models.DrivingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionNovaRequest
        @return: DrivingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.driving_direction_nova_with_options(request, headers, runtime)

    async def driving_direction_nova_async(
        self,
        request: iqs20240712_models.DrivingDirectionNovaRequest,
    ) -> iqs20240712_models.DrivingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的驾车路线规划方案
        
        @param request: DrivingDirectionNovaRequest
        @return: DrivingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.driving_direction_nova_with_options_async(request, headers, runtime)

    def electrobike_direction_with_options(
        self,
        request: iqs20240712_models.ElectrobikeDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.ElectrobikeDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的电动车路线规划方案
        
        @param request: ElectrobikeDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ElectrobikeDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ElectrobikeDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/electrobike',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.ElectrobikeDirectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def electrobike_direction_with_options_async(
        self,
        request: iqs20240712_models.ElectrobikeDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.ElectrobikeDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的电动车路线规划方案
        
        @param request: ElectrobikeDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ElectrobikeDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ElectrobikeDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/electrobike',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.ElectrobikeDirectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def electrobike_direction(
        self,
        request: iqs20240712_models.ElectrobikeDirectionRequest,
    ) -> iqs20240712_models.ElectrobikeDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的电动车路线规划方案
        
        @param request: ElectrobikeDirectionRequest
        @return: ElectrobikeDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.electrobike_direction_with_options(request, headers, runtime)

    async def electrobike_direction_async(
        self,
        request: iqs20240712_models.ElectrobikeDirectionRequest,
    ) -> iqs20240712_models.ElectrobikeDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的电动车路线规划方案
        
        @param request: ElectrobikeDirectionRequest
        @return: ElectrobikeDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.electrobike_direction_with_options_async(request, headers, runtime)

    def electrobike_direction_nova_with_options(
        self,
        request: iqs20240712_models.ElectrobikeDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.ElectrobikeDirectionNovaResponse:
        """
        @summary 电动车路线规划方案V2
        
        @param request: ElectrobikeDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ElectrobikeDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ElectrobikeDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/electrobike',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.ElectrobikeDirectionNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def electrobike_direction_nova_with_options_async(
        self,
        request: iqs20240712_models.ElectrobikeDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.ElectrobikeDirectionNovaResponse:
        """
        @summary 电动车路线规划方案V2
        
        @param request: ElectrobikeDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: ElectrobikeDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ElectrobikeDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/electrobike',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.ElectrobikeDirectionNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def electrobike_direction_nova(
        self,
        request: iqs20240712_models.ElectrobikeDirectionNovaRequest,
    ) -> iqs20240712_models.ElectrobikeDirectionNovaResponse:
        """
        @summary 电动车路线规划方案V2
        
        @param request: ElectrobikeDirectionNovaRequest
        @return: ElectrobikeDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.electrobike_direction_nova_with_options(request, headers, runtime)

    async def electrobike_direction_nova_async(
        self,
        request: iqs20240712_models.ElectrobikeDirectionNovaRequest,
    ) -> iqs20240712_models.ElectrobikeDirectionNovaResponse:
        """
        @summary 电动车路线规划方案V2
        
        @param request: ElectrobikeDirectionNovaRequest
        @return: ElectrobikeDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.electrobike_direction_nova_with_options_async(request, headers, runtime)

    def geo_code_with_options(
        self,
        request: iqs20240712_models.GeoCodeRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.GeoCodeResponse:
        """
        @summary 地理编码，将详细的结构化地址转换为高德经纬度坐标
        
        @param request: GeoCodeRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GeoCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.address):
            query['address'] = request.address
        if not UtilClient.is_unset(request.city):
            query['city'] = request.city
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GeoCode',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/geocode/geo',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.GeoCodeResponse(),
            self.call_api(params, req, runtime)
        )

    async def geo_code_with_options_async(
        self,
        request: iqs20240712_models.GeoCodeRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.GeoCodeResponse:
        """
        @summary 地理编码，将详细的结构化地址转换为高德经纬度坐标
        
        @param request: GeoCodeRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: GeoCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.address):
            query['address'] = request.address
        if not UtilClient.is_unset(request.city):
            query['city'] = request.city
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GeoCode',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/geocode/geo',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.GeoCodeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def geo_code(
        self,
        request: iqs20240712_models.GeoCodeRequest,
    ) -> iqs20240712_models.GeoCodeResponse:
        """
        @summary 地理编码，将详细的结构化地址转换为高德经纬度坐标
        
        @param request: GeoCodeRequest
        @return: GeoCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.geo_code_with_options(request, headers, runtime)

    async def geo_code_async(
        self,
        request: iqs20240712_models.GeoCodeRequest,
    ) -> iqs20240712_models.GeoCodeResponse:
        """
        @summary 地理编码，将详细的结构化地址转换为高德经纬度坐标
        
        @param request: GeoCodeRequest
        @return: GeoCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.geo_code_with_options_async(request, headers, runtime)

    def nearby_search_with_options(
        self,
        request: iqs20240712_models.NearbySearchRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.NearbySearchResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: NearbySearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='NearbySearch',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/pois/nearby',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.NearbySearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def nearby_search_with_options_async(
        self,
        request: iqs20240712_models.NearbySearchRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.NearbySearchResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: NearbySearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='NearbySearch',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/pois/nearby',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.NearbySearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def nearby_search(
        self,
        request: iqs20240712_models.NearbySearchRequest,
    ) -> iqs20240712_models.NearbySearchResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchRequest
        @return: NearbySearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.nearby_search_with_options(request, headers, runtime)

    async def nearby_search_async(
        self,
        request: iqs20240712_models.NearbySearchRequest,
    ) -> iqs20240712_models.NearbySearchResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchRequest
        @return: NearbySearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.nearby_search_with_options_async(request, headers, runtime)

    def nearby_search_nova_with_options(
        self,
        request: iqs20240712_models.NearbySearchNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.NearbySearchNovaResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: NearbySearchNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='NearbySearchNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/pois/nearby',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.NearbySearchNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def nearby_search_nova_with_options_async(
        self,
        request: iqs20240712_models.NearbySearchNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.NearbySearchNovaResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: NearbySearchNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.radius):
            query['radius'] = request.radius
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='NearbySearchNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/pois/nearby',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.NearbySearchNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def nearby_search_nova(
        self,
        request: iqs20240712_models.NearbySearchNovaRequest,
    ) -> iqs20240712_models.NearbySearchNovaResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchNovaRequest
        @return: NearbySearchNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.nearby_search_nova_with_options(request, headers, runtime)

    async def nearby_search_nova_async(
        self,
        request: iqs20240712_models.NearbySearchNovaRequest,
    ) -> iqs20240712_models.NearbySearchNovaResponse:
        """
        @summary 通过经纬度查询附近的地点
        
        @param request: NearbySearchNovaRequest
        @return: NearbySearchNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.nearby_search_nova_with_options_async(request, headers, runtime)

    def place_search_with_options(
        self,
        request: iqs20240712_models.PlaceSearchRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.PlaceSearchResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PlaceSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PlaceSearch',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/pois/place',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.PlaceSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def place_search_with_options_async(
        self,
        request: iqs20240712_models.PlaceSearchRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.PlaceSearchResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PlaceSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PlaceSearch',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/pois/place',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.PlaceSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def place_search(
        self,
        request: iqs20240712_models.PlaceSearchRequest,
    ) -> iqs20240712_models.PlaceSearchResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchRequest
        @return: PlaceSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.place_search_with_options(request, headers, runtime)

    async def place_search_async(
        self,
        request: iqs20240712_models.PlaceSearchRequest,
    ) -> iqs20240712_models.PlaceSearchResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchRequest
        @return: PlaceSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.place_search_with_options_async(request, headers, runtime)

    def place_search_nova_with_options(
        self,
        request: iqs20240712_models.PlaceSearchNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.PlaceSearchNovaResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PlaceSearchNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PlaceSearchNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/pois/place',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.PlaceSearchNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def place_search_nova_with_options_async(
        self,
        request: iqs20240712_models.PlaceSearchNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.PlaceSearchNovaResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: PlaceSearchNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keywords):
            query['keywords'] = request.keywords
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        if not UtilClient.is_unset(request.types):
            query['types'] = request.types
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PlaceSearchNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/pois/place',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.PlaceSearchNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def place_search_nova(
        self,
        request: iqs20240712_models.PlaceSearchNovaRequest,
    ) -> iqs20240712_models.PlaceSearchNovaResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchNovaRequest
        @return: PlaceSearchNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.place_search_nova_with_options(request, headers, runtime)

    async def place_search_nova_async(
        self,
        request: iqs20240712_models.PlaceSearchNovaRequest,
    ) -> iqs20240712_models.PlaceSearchNovaResponse:
        """
        @summary 通过关键词搜索地点
        
        @param request: PlaceSearchNovaRequest
        @return: PlaceSearchNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.place_search_nova_with_options_async(request, headers, runtime)

    def query_attractions_with_options(
        self,
        request: iqs20240712_models.QueryAttractionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryAttractionsResponse:
        """
        @summary 景点查询
        
        @param request: QueryAttractionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryAttractionsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryAttractions',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/attractions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryAttractionsResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_attractions_with_options_async(
        self,
        request: iqs20240712_models.QueryAttractionsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryAttractionsResponse:
        """
        @summary 景点查询
        
        @param request: QueryAttractionsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryAttractionsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryAttractions',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/attractions',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryAttractionsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_attractions(
        self,
        request: iqs20240712_models.QueryAttractionsRequest,
    ) -> iqs20240712_models.QueryAttractionsResponse:
        """
        @summary 景点查询
        
        @param request: QueryAttractionsRequest
        @return: QueryAttractionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.query_attractions_with_options(request, headers, runtime)

    async def query_attractions_async(
        self,
        request: iqs20240712_models.QueryAttractionsRequest,
    ) -> iqs20240712_models.QueryAttractionsResponse:
        """
        @summary 景点查询
        
        @param request: QueryAttractionsRequest
        @return: QueryAttractionsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.query_attractions_with_options_async(request, headers, runtime)

    def query_hotels_with_options(
        self,
        request: iqs20240712_models.QueryHotelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryHotelsResponse:
        """
        @summary 酒店查询
        
        @param request: QueryHotelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryHotelsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryHotels',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/hotels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryHotelsResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_hotels_with_options_async(
        self,
        request: iqs20240712_models.QueryHotelsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryHotelsResponse:
        """
        @summary 酒店查询
        
        @param request: QueryHotelsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryHotelsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryHotels',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/hotels',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryHotelsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_hotels(
        self,
        request: iqs20240712_models.QueryHotelsRequest,
    ) -> iqs20240712_models.QueryHotelsResponse:
        """
        @summary 酒店查询
        
        @param request: QueryHotelsRequest
        @return: QueryHotelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.query_hotels_with_options(request, headers, runtime)

    async def query_hotels_async(
        self,
        request: iqs20240712_models.QueryHotelsRequest,
    ) -> iqs20240712_models.QueryHotelsResponse:
        """
        @summary 酒店查询
        
        @param request: QueryHotelsRequest
        @return: QueryHotelsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.query_hotels_with_options_async(request, headers, runtime)

    def query_restaurants_with_options(
        self,
        request: iqs20240712_models.QueryRestaurantsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryRestaurantsResponse:
        """
        @summary 餐厅查询
        
        @param request: QueryRestaurantsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryRestaurantsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryRestaurants',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/restaurants',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryRestaurantsResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_restaurants_with_options_async(
        self,
        request: iqs20240712_models.QueryRestaurantsRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.QueryRestaurantsResponse:
        """
        @summary 餐厅查询
        
        @param request: QueryRestaurantsRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryRestaurantsResponse
        """
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            headers=headers,
            body=OpenApiUtilClient.parse_to_map(request.body)
        )
        params = open_api_models.Params(
            action='QueryRestaurants',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/amap-function-call-agent/iqs-agent-service/v1/nl/restaurants',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.QueryRestaurantsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_restaurants(
        self,
        request: iqs20240712_models.QueryRestaurantsRequest,
    ) -> iqs20240712_models.QueryRestaurantsResponse:
        """
        @summary 餐厅查询
        
        @param request: QueryRestaurantsRequest
        @return: QueryRestaurantsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.query_restaurants_with_options(request, headers, runtime)

    async def query_restaurants_async(
        self,
        request: iqs20240712_models.QueryRestaurantsRequest,
    ) -> iqs20240712_models.QueryRestaurantsResponse:
        """
        @summary 餐厅查询
        
        @param request: QueryRestaurantsRequest
        @return: QueryRestaurantsResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.query_restaurants_with_options_async(request, headers, runtime)

    def rectangle_traffic_status_with_options(
        self,
        request: iqs20240712_models.RectangleTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RectangleTrafficStatusResponse:
        """
        @summary 实时查询矩形区域内的交通信息查询
        
        @param request: RectangleTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RectangleTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.lower_left_latitude):
            query['lowerLeftLatitude'] = request.lower_left_latitude
        if not UtilClient.is_unset(request.lower_left_longitude):
            query['lowerLeftLongitude'] = request.lower_left_longitude
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        if not UtilClient.is_unset(request.upper_right_latitude):
            query['upperRightLatitude'] = request.upper_right_latitude
        if not UtilClient.is_unset(request.upper_right_longitude):
            query['upperRightLongitude'] = request.upper_right_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RectangleTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/rectangle',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RectangleTrafficStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def rectangle_traffic_status_with_options_async(
        self,
        request: iqs20240712_models.RectangleTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RectangleTrafficStatusResponse:
        """
        @summary 实时查询矩形区域内的交通信息查询
        
        @param request: RectangleTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RectangleTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.lower_left_latitude):
            query['lowerLeftLatitude'] = request.lower_left_latitude
        if not UtilClient.is_unset(request.lower_left_longitude):
            query['lowerLeftLongitude'] = request.lower_left_longitude
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        if not UtilClient.is_unset(request.upper_right_latitude):
            query['upperRightLatitude'] = request.upper_right_latitude
        if not UtilClient.is_unset(request.upper_right_longitude):
            query['upperRightLongitude'] = request.upper_right_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RectangleTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/rectangle',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RectangleTrafficStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def rectangle_traffic_status(
        self,
        request: iqs20240712_models.RectangleTrafficStatusRequest,
    ) -> iqs20240712_models.RectangleTrafficStatusResponse:
        """
        @summary 实时查询矩形区域内的交通信息查询
        
        @param request: RectangleTrafficStatusRequest
        @return: RectangleTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.rectangle_traffic_status_with_options(request, headers, runtime)

    async def rectangle_traffic_status_async(
        self,
        request: iqs20240712_models.RectangleTrafficStatusRequest,
    ) -> iqs20240712_models.RectangleTrafficStatusResponse:
        """
        @summary 实时查询矩形区域内的交通信息查询
        
        @param request: RectangleTrafficStatusRequest
        @return: RectangleTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.rectangle_traffic_status_with_options_async(request, headers, runtime)

    def rgeo_code_with_options(
        self,
        request: iqs20240712_models.RgeoCodeRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RgeoCodeResponse:
        """
        @summary 逆地理编码，将经纬度转换为详细结构化的地址信息
        
        @param request: RgeoCodeRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RgeoCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RgeoCode',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/geocode/regeo',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RgeoCodeResponse(),
            self.call_api(params, req, runtime)
        )

    async def rgeo_code_with_options_async(
        self,
        request: iqs20240712_models.RgeoCodeRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RgeoCodeResponse:
        """
        @summary 逆地理编码，将经纬度转换为详细结构化的地址信息
        
        @param request: RgeoCodeRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RgeoCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.latitude):
            query['latitude'] = request.latitude
        if not UtilClient.is_unset(request.longitude):
            query['longitude'] = request.longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RgeoCode',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/geocode/regeo',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RgeoCodeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def rgeo_code(
        self,
        request: iqs20240712_models.RgeoCodeRequest,
    ) -> iqs20240712_models.RgeoCodeResponse:
        """
        @summary 逆地理编码，将经纬度转换为详细结构化的地址信息
        
        @param request: RgeoCodeRequest
        @return: RgeoCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.rgeo_code_with_options(request, headers, runtime)

    async def rgeo_code_async(
        self,
        request: iqs20240712_models.RgeoCodeRequest,
    ) -> iqs20240712_models.RgeoCodeResponse:
        """
        @summary 逆地理编码，将经纬度转换为详细结构化的地址信息
        
        @param request: RgeoCodeRequest
        @return: RgeoCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.rgeo_code_with_options_async(request, headers, runtime)

    def road_traffic_status_with_options(
        self,
        request: iqs20240712_models.RoadTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RoadTrafficStatusResponse:
        """
        @summary 实时查询指定线路的交通信息
        
        @param request: RoadTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RoadTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.city):
            query['city'] = request.city
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        if not UtilClient.is_unset(request.road_name):
            query['roadName'] = request.road_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RoadTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/road',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RoadTrafficStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def road_traffic_status_with_options_async(
        self,
        request: iqs20240712_models.RoadTrafficStatusRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.RoadTrafficStatusResponse:
        """
        @summary 实时查询指定线路的交通信息
        
        @param request: RoadTrafficStatusRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: RoadTrafficStatusResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.city):
            query['city'] = request.city
        if not UtilClient.is_unset(request.road_level):
            query['roadLevel'] = request.road_level
        if not UtilClient.is_unset(request.road_name):
            query['roadName'] = request.road_name
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RoadTrafficStatus',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/traffic/status/road',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.RoadTrafficStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def road_traffic_status(
        self,
        request: iqs20240712_models.RoadTrafficStatusRequest,
    ) -> iqs20240712_models.RoadTrafficStatusResponse:
        """
        @summary 实时查询指定线路的交通信息
        
        @param request: RoadTrafficStatusRequest
        @return: RoadTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.road_traffic_status_with_options(request, headers, runtime)

    async def road_traffic_status_async(
        self,
        request: iqs20240712_models.RoadTrafficStatusRequest,
    ) -> iqs20240712_models.RoadTrafficStatusResponse:
        """
        @summary 实时查询指定线路的交通信息
        
        @param request: RoadTrafficStatusRequest
        @return: RoadTrafficStatusResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.road_traffic_status_with_options_async(request, headers, runtime)

    def transit_integrated_direction_with_options(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.TransitIntegratedDirectionResponse:
        """
        @summary 公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: TransitIntegratedDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_city):
            query['destinationCity'] = request.destination_city
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_city):
            query['originCity'] = request.origin_city
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TransitIntegratedDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/transit/integrated',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.TransitIntegratedDirectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def transit_integrated_direction_with_options_async(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.TransitIntegratedDirectionResponse:
        """
        @summary 公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: TransitIntegratedDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_city):
            query['destinationCity'] = request.destination_city
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_city):
            query['originCity'] = request.origin_city
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TransitIntegratedDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/transit/integrated',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.TransitIntegratedDirectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def transit_integrated_direction(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionRequest,
    ) -> iqs20240712_models.TransitIntegratedDirectionResponse:
        """
        @summary 公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionRequest
        @return: TransitIntegratedDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.transit_integrated_direction_with_options(request, headers, runtime)

    async def transit_integrated_direction_async(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionRequest,
    ) -> iqs20240712_models.TransitIntegratedDirectionResponse:
        """
        @summary 公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionRequest
        @return: TransitIntegratedDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.transit_integrated_direction_with_options_async(request, headers, runtime)

    def transit_integrated_direction_old_with_options(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionOldRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.TransitIntegratedDirectionOldResponse:
        """
        @summary 根据起终点坐标检索符合条件的公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionOldRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: TransitIntegratedDirectionOldResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_city):
            query['destinationCity'] = request.destination_city
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_city):
            query['originCity'] = request.origin_city
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TransitIntegratedDirectionOld',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/transit/integrated',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.TransitIntegratedDirectionOldResponse(),
            self.call_api(params, req, runtime)
        )

    async def transit_integrated_direction_old_with_options_async(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionOldRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.TransitIntegratedDirectionOldResponse:
        """
        @summary 根据起终点坐标检索符合条件的公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionOldRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: TransitIntegratedDirectionOldResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_city):
            query['destinationCity'] = request.destination_city
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_city):
            query['originCity'] = request.origin_city
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TransitIntegratedDirectionOld',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/transit/integrated',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.TransitIntegratedDirectionOldResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def transit_integrated_direction_old(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionOldRequest,
    ) -> iqs20240712_models.TransitIntegratedDirectionOldResponse:
        """
        @summary 根据起终点坐标检索符合条件的公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionOldRequest
        @return: TransitIntegratedDirectionOldResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.transit_integrated_direction_old_with_options(request, headers, runtime)

    async def transit_integrated_direction_old_async(
        self,
        request: iqs20240712_models.TransitIntegratedDirectionOldRequest,
    ) -> iqs20240712_models.TransitIntegratedDirectionOldResponse:
        """
        @summary 根据起终点坐标检索符合条件的公共交通路线规划方案
        
        @param request: TransitIntegratedDirectionOldRequest
        @return: TransitIntegratedDirectionOldResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.transit_integrated_direction_old_with_options_async(request, headers, runtime)

    def walking_direction_with_options(
        self,
        request: iqs20240712_models.WalkingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.WalkingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: WalkingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WalkingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/walking',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.WalkingDirectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def walking_direction_with_options_async(
        self,
        request: iqs20240712_models.WalkingDirectionRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.WalkingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: WalkingDirectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WalkingDirection',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v1/direction/walking',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.WalkingDirectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def walking_direction(
        self,
        request: iqs20240712_models.WalkingDirectionRequest,
    ) -> iqs20240712_models.WalkingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionRequest
        @return: WalkingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.walking_direction_with_options(request, headers, runtime)

    async def walking_direction_async(
        self,
        request: iqs20240712_models.WalkingDirectionRequest,
    ) -> iqs20240712_models.WalkingDirectionResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionRequest
        @return: WalkingDirectionResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.walking_direction_with_options_async(request, headers, runtime)

    def walking_direction_nova_with_options(
        self,
        request: iqs20240712_models.WalkingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.WalkingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: WalkingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WalkingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/walking',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.WalkingDirectionNovaResponse(),
            self.call_api(params, req, runtime)
        )

    async def walking_direction_nova_with_options_async(
        self,
        request: iqs20240712_models.WalkingDirectionNovaRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> iqs20240712_models.WalkingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionNovaRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: WalkingDirectionNovaResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.destination_latitude):
            query['destinationLatitude'] = request.destination_latitude
        if not UtilClient.is_unset(request.destination_longitude):
            query['destinationLongitude'] = request.destination_longitude
        if not UtilClient.is_unset(request.origin_latitude):
            query['originLatitude'] = request.origin_latitude
        if not UtilClient.is_unset(request.origin_longitude):
            query['originLongitude'] = request.origin_longitude
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WalkingDirectionNova',
            version='2024-07-12',
            protocol='HTTPS',
            pathname=f'/ipaas/v2/direction/walking',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            iqs20240712_models.WalkingDirectionNovaResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def walking_direction_nova(
        self,
        request: iqs20240712_models.WalkingDirectionNovaRequest,
    ) -> iqs20240712_models.WalkingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionNovaRequest
        @return: WalkingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.walking_direction_nova_with_options(request, headers, runtime)

    async def walking_direction_nova_async(
        self,
        request: iqs20240712_models.WalkingDirectionNovaRequest,
    ) -> iqs20240712_models.WalkingDirectionNovaResponse:
        """
        @summary 根据起终点坐标检索符合条件的步行路线规划方案
        
        @param request: WalkingDirectionNovaRequest
        @return: WalkingDirectionNovaResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.walking_direction_nova_with_options_async(request, headers, runtime)
