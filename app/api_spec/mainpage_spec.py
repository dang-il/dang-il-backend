class MainpageSpec:
    @staticmethod
    def mainpage():
        spec = {
            "summary": "메인페이지 초기 로딩에 필요한 정보 응답",
            "description": 
                """
                    로그인 한 상태로 요청 시 메인페이지 초기 로딩에 필요한 정보 응답 <br><br>  
                    본인+친구+모르는 사람 포함해서 18명 응답 <br><br>
                    모르는 사람은 18-(본인+친구) 형태로 반환 <br><br>
                    공간 정보, 집중 시간 정보도 응답
                """,
            "operation_id": "mainpage",
            "responses": {
                200: {
                    "description": "메시지, 각 유저의 사용자 정보, 공간 정보, 집중 시간 정보 포함된 응답",
                    "content": {
                            "application/json": {
                                "examples": {
                                    "회원가입 예시": {
                                        "summary": "회원가입 예시",
                                        "value": {
                                            "message": "register process is complete",
                                            "data": {}
                                        }
                                    },
                                }
                            }
                        }
                    },
                }
            }
        return spec