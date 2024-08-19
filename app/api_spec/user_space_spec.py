class UserSpaceSpec:
    @staticmethod
    def space():
        spec = {
            "summary": "경로 파라미터에 들어있는 id의 유저 공간 불러오는 엔드포인트(테스트X)",
            "description": 
                """
                    path_user_id에 값을 넣어 해당 id의 유저 공간+작업 시간을 불러오는 엔드포인트 <br><br>  
                    본인, 친구, 접근을 허용해둔(accessbility가 true) 모르는 사람의 공간정보+작업시간 정보 불러옴 <br><br> 
                    본인, 친구 검증을 위해 쿠키에 session_id 필수
                """,
            "operation_id": "space",
            "responses": {
                200: {
                    "description": "메시지, data(안에 공간 정보, 작업 시간 정보)",
                    "content": {
                            "application/json": {
                                "examples": {
                                    "응답 예시": {
                                        "summary": "응답 예시",
                                        "value": {
                                            {
                                                "message": "data successfully transferred",
                                                "data": {
                                                    "accessibility": True,
                                                    "user_space_data": {
                                                        "_id": "test1",
                                                        "interior_data": [
                                                            {
                                                                "decor_id": "desk1",
                                                                "location": [
                                                                    1.0,
                                                                    2.0,
                                                                    3.0
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    "user_tasking_time_data": {
                                                        "_id": "test1",
                                                        "today_tasking_time": {
                                                            "total_time": 3600,
                                                            "task_specific_time": {
                                                                "math": 1900,
                                                                "coding": 1700
                                                            }
                                                        },
                                                        "previous_tasking_time": {
                                                            "day1": {
                                                                "total_time": 10800,
                                                                "task_specific_time": {
                                                                    "math": 5400,
                                                                    "coding": 5400
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                }
                            }
                        }
                    },
                }
            }
        return spec
