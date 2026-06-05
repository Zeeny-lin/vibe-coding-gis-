"""
GIS空间分析服务
提供核心地理空间分析功能
"""
import json
import math
import os
import requests
from pathlib import Path
from typing import List, Optional, Dict, Any
from app.core.config import settings


class GISService:
    """GIS空间分析服务类"""
    
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        # 从配置中读取高德地图API密钥
        self.amap_key = settings.AMAP_API_KEY if hasattr(settings, 'AMAP_API_KEY') and settings.AMAP_API_KEY else os.getenv('AMAP_API_KEY')
    
    def _load_poi_data(self, poi_type: str = None) -> Dict:
        """加载POI数据"""
        poi_dir = self.data_dir / "poi"
        
        if poi_type:
            data_file = poi_dir / f"{poi_type}.geojson"
            if data_file.exists():
                with open(data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        
        # 加载所有POI
        all_features = []
        if poi_dir.exists():
            for file in poi_dir.glob("*.geojson"):
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_features.extend(data.get("features", []))
        
        return {"type": "FeatureCollection", "features": all_features}
    
    def _calculate_distance(self, point1: List[float], point2: List[float]) -> float:
        """
        使用Haversine公式计算两点间的距离（米）
        point格式: [经度, 纬度]
        """
        R = 6371000  # 地球半径（米）
        
        lon1, lat1 = math.radians(point1[0]), math.radians(point1[1])
        lon2, lat2 = math.radians(point2[0]), math.radians(point2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _get_amap_route(self, start: List[float], end: List[float], mode: str = "driving") -> Dict:
        """
        调用高德地图API获取规划路径 (真实导航)
        支持多种出行方式: driving(驾车), walking(步行), transit(公交), cycling(骑行)
        """
        if not self.amap_key:
            return None
            
        # 坐标转换：start, end 已经是GCJ-02 (因为前端和fetch脚本都统一了) 或 WGS84
        # 高德Web服务需要 经度,纬度
        origin = f"{start[0]:.6f},{start[1]:.6f}"
        destination = f"{end[0]:.6f},{end[1]:.6f}"
        
        # 根据出行方式选择不同的API
        mode_config = {
            "driving": {
                "url": "https://restapi.amap.com/v3/direction/driving",
                "params": {
                    'key': self.amap_key,
                    'origin': origin,
                    'destination': destination,
                    'extensions': 'base',
                    'strategy': 10  # 速度优先
                }
            },
            "walking": {
                "url": "https://restapi.amap.com/v3/direction/walking",
                "params": {
                    'key': self.amap_key,
                    'origin': origin,
                    'destination': destination
                }
            },
            "cycling": {
                "url": "https://restapi.amap.com/v4/direction/bicycling",
                "params": {
                    'key': self.amap_key,
                    'origin': origin,
                    'destination': destination
                }
            },
            "transit": {
                "url": "https://restapi.amap.com/v3/direction/transit/integrated",
                "params": {
                    'key': self.amap_key,
                    'origin': origin,
                    'destination': destination,
                    'city': '莆田',
                    'cityd': '莆田',
                    'strategy': 0  # 最快捷
                }
            }
        }
        
        config = mode_config.get(mode, mode_config["driving"])
        url = config["url"]
        params = config["params"]
        
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            
            # 不同模式的响应解析
            if mode == "cycling":
                # 骑行API v4 返回格式不同
                if data.get('errcode') == 0 and data.get('data', {}).get('paths'):
                    route_path = data['data']['paths'][0]
                    distance = int(route_path.get('distance', 0))
                    duration = int(route_path.get('duration', 0))
                    
                    path_coords = []
                    for step in route_path.get('steps', []):
                        polyline = step.get('polyline', '')
                        if polyline:
                            points = polyline.split(';')
                            for p in points:
                                lng, lat = map(float, p.split(','))
                                path_coords.append([lng, lat])
                    
                    return {
                        "distance": distance,
                        "duration": duration,
                        "coords": path_coords,
                        "mode": mode
                    }
            elif mode == "transit":
                # 公交换乘返回格式复杂，简化处理
                if data['status'] == '1' and data.get('route', {}).get('transits'):
                    transit = data['route']['transits'][0]
                    distance = int(data['route'].get('distance', 0))
                    duration = int(transit.get('duration', 0))
                    
                    # 公交路线只取起终点连线
                    path_coords = [[start[0], start[1]], [end[0], end[1]]]
                    
                    return {
                        "distance": distance,
                        "duration": duration,
                        "coords": path_coords,
                        "mode": mode,
                        "transit_info": transit.get('walking_distance', 0)
                    }
            else:
                # 驾车/步行 API v3 返回格式
                if data['status'] == '1' and int(data.get('count', 0)) > 0:
                    route_path = data['route']['paths'][0]
                    distance = int(route_path['distance'])
                    duration = int(route_path['duration'])
                    
                    # 解析geometry
                    path_coords = []
                    for step in route_path['steps']:
                        polyline = step['polyline']
                        # "119.1,25.1;119.2,25.2"
                        points = polyline.split(';')
                        for p in points:
                            lng, lat = map(float, p.split(','))
                            path_coords.append([lng, lat])
                            
                    return {
                        "distance": distance,  # meters
                        "duration": duration,  # seconds
                        "coords": path_coords,
                        "mode": mode
                    }
        except Exception as e:
            print(f"Amap Route Error ({mode}): {e}")
            
        return None

    def plan_route(self, start: List[float], end: List[float], 
                   waypoints: Optional[List[List[float]]] = None,
                   mode: str = "driving") -> Dict:
        """
        路线规划
        支持多种出行方式: driving(驾车), walking(步行), transit(公交), cycling(骑行)
        使用最近邻算法近似求解TSP问题，并结合高德API进行真实路径规划
        """
        points = [start]
        if waypoints:
            points.extend(waypoints)
        points.append(end)
        
        # ... (简化的最近邻排序，保持不变) ...
        # 如果点少于等于2，直接按顺序
        if len(points) <= 2:
            optimized_route = points
        else:
             # 最近邻算法规划路线
            visited = [False] * len(points)
            route_idx = [0]  # 从起点开始
            visited[0] = True
            
            # 确保终点最后访问
            end_idx = len(points) - 1
            
            current = 0
            while len(route_idx) < len(points) - 1:
                nearest = None
                min_dist = float('inf')
                
                for i in range(1, len(points) - 1):  # 排除终点
                    if not visited[i]:
                        dist = self._calculate_distance(points[current], points[i])
                        if dist < min_dist:
                            min_dist = dist
                            nearest = i
                
                if nearest is not None:
                    route_idx.append(nearest)
                    visited[nearest] = True
                    current = nearest
            
            route_idx.append(end_idx)  # 最后添加终点
            optimized_route = [points[i] for i in route_idx]

        
        # 计算总距离和分段信息 (使用高德API)
        total_distance = 0
        total_duration = 0
        segments = []
        full_path_coords = []
        
        # 速度估算（作为降级方案）
        speed_mps = {
            "driving": 13.8,   # 50km/h
            "walking": 1.4,    # 5km/h
            "cycling": 4.2,    # 15km/h
            "transit": 8.3     # 30km/h
        }
        
        for i in range(len(optimized_route) - 1):
            p1 = optimized_route[i]
            p2 = optimized_route[i+1]
            
            # 尝试获取真实路径（传递出行方式）
            real_route = self._get_amap_route(p1, p2, mode)
            
            if real_route:
                dist = real_route['distance']
                dur = real_route['duration']
                seg_coords = real_route['coords']
            else:
                # 降级为直线
                dist = self._calculate_distance(p1, p2)
                dur = dist / speed_mps.get(mode, 13.8)
                seg_coords = [p1, p2]
            
            total_distance += dist
            total_duration += dur
            full_path_coords.extend(seg_coords)
            
            segments.append({
                "from": p1,
                "to": p2,
                "distance": round(dist, 2),
                "duration": round(dur / 60, 1),
                "geometry": seg_coords
            })
        
        # 出行方式中文名称
        mode_names = {
            "driving": "驾车",
            "walking": "步行",
            "cycling": "骑行",
            "transit": "公交"
        }
        
        return {
            "route_order": optimized_route, # 优化的访问点顺序
            "route_path": full_path_coords, # 用于绘制的完整线串
            "total_distance": round(total_distance, 2),
            "estimated_time": round(total_duration / 60, 1),  # 分钟
            "segments": segments,
            "mode": mode,
            "mode_name": mode_names.get(mode, "驾车")
        }
    
    def site_selection(self, facility_type: str, weights: Optional[Dict] = None) -> Dict:
        """
        智能选址推荐
        使用加权叠加分析方法
        """
        # 默认权重
        default_weights = {
            "population": 0.3,      # 人口密度
            "accessibility": 0.25,  # 交通便利度
            "competition": 0.25,    # 竞争距离
            "tourism": 0.2          # 旅游热度
        }
        weights = weights or default_weights
        
        # 加载统计数据
        stats_file = self.data_dir / "statistics.json"
        if stats_file.exists():
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = {"districts": []}
        
        # 计算各区县得分
        recommendations = []
        for district in stats.get("districts", []):
            # 简化的评分模型
            pop_score = min((district.get("population", 0) / 100) * 100, 100)
            gdp_score = min((district.get("gdp", 0) / 500) * 100, 100)
            
            # 综合得分
            total_score = (
                pop_score * weights.get("population", 0.3) +
                gdp_score * weights.get("accessibility", 0.25) +
                50 * weights.get("competition", 0.25) +  # 假设中等竞争
                60 * weights.get("tourism", 0.2)  # 假设中等旅游热度
            )
            
            recommendations.append({
                "district": district.get("name"),
                "score": round(total_score, 2),
                "factors": {
                    "population_score": round(pop_score, 2),
                    "gdp_score": round(gdp_score, 2)
                }
            })
        
        # 按得分排序
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "facility_type": facility_type,
            "weights": weights,
            "recommendations": recommendations[:5],  # 返回前5个推荐
            "best_location": recommendations[0] if recommendations else None
        }
    
    def accessibility_analysis(self, poi_type: str, threshold: int = 3000) -> Dict:
        """
        可达性分析
        计算各区县到指定类型设施的可达性
        """
        poi_data = self._load_poi_data(poi_type)
        poi_features = poi_data.get("features", [])
        
        # 加载区县数据
        districts_file = self.data_dir / "districts.geojson"
        if districts_file.exists():
            with open(districts_file, "r", encoding="utf-8") as f:
                districts = json.load(f)
        else:
            districts = {"features": []}
        
        results = []
        for district in districts.get("features", []):
            name = district.get("properties", {}).get("name", "未知")
            
            # 计算该区县内的POI数量（简化处理）
            poi_count = sum(
                1 for poi in poi_features 
                if poi.get("properties", {}).get("district") == name
            )
            
            # 可达性评级
            if poi_count >= 5:
                accessibility = "优秀"
                score = 90
            elif poi_count >= 3:
                accessibility = "良好"
                score = 70
            elif poi_count >= 1:
                accessibility = "一般"
                score = 50
            else:
                accessibility = "较差"
                score = 30
            
            results.append({
                "district": name,
                "poi_count": poi_count,
                "accessibility": accessibility,
                "score": score
            })
        
        # 计算整体评估
        avg_score = sum(r["score"] for r in results) / len(results) if results else 0
        
        return {
            "poi_type": poi_type,
            "threshold": threshold,
            "district_results": results,
            "overall_score": round(avg_score, 2),
            "coverage_assessment": "均衡" if avg_score >= 70 else "需改善"
        }
    
    def service_coverage(self, poi_type: str, buffer_distance: int = 2000) -> Dict:
        """
        公共服务覆盖分析
        """
        poi_data = self._load_poi_data(poi_type)
        poi_features = poi_data.get("features", [])
        
        # 生成服务覆盖区域（简化为圆形缓冲区）
        coverage_areas = []
        for poi in poi_features:
            coords = poi.get("geometry", {}).get("coordinates", [0, 0])
            coverage_areas.append({
                "center": coords,
                "radius": buffer_distance,
                "name": poi.get("properties", {}).get("name", "未知")
            })
        
        return {
            "poi_type": poi_type,
            "buffer_distance": buffer_distance,
            "total_facilities": len(poi_features),
            "coverage_areas": coverage_areas,
            "analysis_note": f"共{len(poi_features)}个{poi_type}类设施，服务半径{buffer_distance}米"
        }
    
    def density_analysis(self, poi_type: str, cell_size: int = 1000) -> Dict:
        """
        密度分析
        生成热力图数据
        """
        poi_data = self._load_poi_data(poi_type)
        poi_features = poi_data.get("features", [])
        
        # 生成热力图点数据
        heat_points = []
        for poi in poi_features:
            coords = poi.get("geometry", {}).get("coordinates", [0, 0])
            heat_points.append({
                "lng": coords[0],
                "lat": coords[1],
                "weight": 1
            })
        
        return {
            "poi_type": poi_type,
            "cell_size": cell_size,
            "total_points": len(heat_points),
            "heat_data": heat_points
        }
    
    def tourism_route(self, theme: str = "mazu", duration: int = 1) -> Dict:
        """
        旅游路线推荐
        """
        # 预定义的妈祖文化旅游路线
        mazu_routes = {
            1: {
                "name": "妈祖朝圣一日游",
                "spots": [
                    {"name": "湄洲妈祖祖庙", "coords": [119.145120, 25.090959], "duration": 120, "description": "妈祖祖庙，朝圣圣地"},
                    {"name": "天妃故里", "coords": [119.138056, 25.089201], "duration": 60, "description": "妈祖林默娘出生地"},
                    {"name": "妈祖文化园", "coords": [119.146000, 25.092000], "duration": 90, "description": "了解妈祖文化"},
                    {"name": "湄洲岛黄金沙滩", "coords": [119.103421, 25.046464], "duration": 60, "description": "休闲放松"}
                ],
                "total_duration": 330,
                "description": "深度体验妈祖文化的经典一日游路线"
            },
            2: {
                "name": "妈祖文化深度两日游",
                "spots": [
                    {"name": "湄洲妈祖祖庙", "coords": [119.145120, 25.090959], "duration": 150, "description": "朝圣参拜"},
                    {"name": "妈祖影视城", "coords": [119.130928, 25.043880], "duration": 90, "description": "影视文化体验"},
                    {"name": "九鲤湖", "coords": [118.821591, 25.460157], "duration": 180, "description": "九鲤飞瀑"},
                    {"name": "广化寺", "coords": [118.988960, 25.425153], "duration": 90, "description": "千年古刹"},
                    {"name": "南少林寺", "coords": [119.041044, 25.539635], "duration": 120, "description": "武术圣地"}
                ],
                "total_duration": 630,
                "description": "结合妈祖文化与自然风光的深度游"
            }
        }
        
        route = mazu_routes.get(duration, mazu_routes[1])
        
        # 计算路线
        spots = route["spots"]
        route_coords = [spot["coords"] for spot in spots]
        
        # 使用 plan_route 获取真实导航路径
        full_route = self.plan_route(
            start=route_coords[0],
            end=route_coords[-1],
            waypoints=route_coords[1:-1] if len(route_coords) > 2 else None
        )
        
        return {
            "theme": theme,
            "duration": duration,
            "route_name": route["name"],
            "description": route["description"],
            "spots": spots,
            "route_line": full_route["route_path"], # 使用真实导航路径
            "total_distance": round(full_route["total_distance"] / 1000, 2),  # 公里
            "total_duration": int(full_route["estimated_time"])
        }
