# LiviDuvy — 리비두비

Unity WebGL 게임 배포 저장소입니다. Unity 프로젝트 원본은 로컬 작업 프로젝트에 보존합니다.

실제 WebGL 빌드를 검증한 뒤 `LiviDuvy-WebGL.zip`을 GitHub Release에 올리고,
`Publish LiviDuvy WebGL` 워크플로에 해당 릴리스 태그를 입력합니다.
워크플로는 빌드 파일 구조를 검사한 후 GitHub Pages에 배포합니다.
대용량 Unity 빌드 파일을 Git 커밋에 직접 넣지 않습니다.

빌드에는 GitHub Pages에서 사용할 수 있는 압축 설정, 상대 URL, 브라우저 영상·오디오 입력 처리가 필요합니다.
`tools/verify_site.py`는 파일 구조 검사만 수행합니다. 온보딩, 캐릭터, 카메라, 가구 배치,
커서, 사운드의 Chrome·Safari 실제 플레이 검증을 별도로 완료해야 합니다.
