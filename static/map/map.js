var mapContainer = document.getElementById('map'); 
var mapOption = {
    center: new kakao.maps.LatLng(33.450701, 126.570667), // 초기 중심 좌표 (임시)
    level: 3 // 지도 확대 레벨
};

// 지도 생성 
var map = new kakao.maps.Map(mapContainer, mapOption); 

// 주소-좌표 변환 객체 생성
var geocoder = new kakao.maps.services.Geocoder();

// 서버에서 전달된 주소로 좌표 검색
geocoder.addressSearch(storeAddress, function(result, status) {
    if (status === kakao.maps.services.Status.OK) {
        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치 표시합니다
        var marker = new kakao.maps.Marker({
            map: map,
            position: coords
        });

        // 마커 텍스트
        var infowindow = new kakao.maps.InfoWindow({
            content: `<div style="width:150px;text-align:center;padding:6px 0;">${storeName}</div>`
        });
        infowindow.open(map, marker);
    }
});