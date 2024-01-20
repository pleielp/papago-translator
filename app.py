from flask import Flask, request, jsonify, make_response
import requests
import os
from dotenv import load_dotenv
from logger_config import get_logger


load_dotenv()

app = Flask(__name__)
get_logger(__name__)

@app.route("/translate", methods=['POST'])
def translate():
    if request.method == 'POST':
        app.logger.info(f"[{request.method}] {request.path}]")
        app.logger.debug(f"request form: {request.form}")

        # 파라미터 가져오기
        text = request.form.get('text')
        source = request.form.get('source')
        target = request.form.get('target')

        # 파라미터 체크
        if text is None or text == '':
            res = jsonify({'result': 'error', 'msg': 'text parameter is needed (text 파라미터가 필요합니다.)'})
            res.status_code = 400
            return res
        if source is None or source == '':
            try:
                # 파파고 언어 감지 API 호출
                source = autodetect_using_naver(text)
            except Exception as e:
                res = jsonify({'result': 'error', 'msg': e.args[1]})
                res.status_code = e.args[0]
                return res
        if target is None or target == '':
            target = 'en' if source == 'ko' else 'ko'

        # 파파고 번역 API 호출
        try:
            res = translate_using_naver(text, source, target)
            res = jsonify(res)
            res.headers.add('Access-Control-Allow-Origin', '*')
        except Exception as e:
            res = jsonify({'result': 'error', 'msg': e.args[1]})
            res.status_code = e.args[0]
            return res
        
        return res

def autodetect_using_naver(text: str) -> str:
    autodetect_url = os.environ.get('NAVER_AUTODETECT_URL')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'X-Naver-Client-Id': os.getenv('NAVER_CLIENT_ID'),
        'X-Naver-Client-Secret': os.getenv('NAVER_CLIENT_SECRET'),
    }
    data = {
        "query": text
    }
    app.logger.debug(f"naver autodetect req: {data}")

    res = requests.post(
        url=autodetect_url,
        headers=headers,
        data=data
    )
    app.logger.debug(f"naver autodetect res: [{res.status_code}] {res.json()}")

    if res.status_code != 200:
        raise Exception(res.status_code, f"{res.json()['errorMessage']}")

    result = res.json()['langCode']
    app.logger.debug(f"naver autodetect result: {result}")

    return result

def translate_using_naver(text, source, target) -> dict:
    translate_url = os.environ.get('NAVER_TRANSLATE_URL')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'X-Naver-Client-Id': os.getenv('NAVER_CLIENT_ID'),
        'X-Naver-Client-Secret': os.getenv('NAVER_CLIENT_SECRET'),
    }

    data = {
        'source': source,
        'target': target,
        'text': text,
    }
    app.logger.debug(f"naver translate req: {data}")
    res = requests.post(
        url=translate_url,
        headers=headers,
        data=data
    )
    app.logger.debug(f"naver translate res: [{res.status_code}] {res.json()}")

    if res.status_code != 200:
        raise Exception(res.status_code, f"{res.json()['errorMessage']}")

    result = res.json()
    app.logger.debug(f"naver translate result: {result}")

    return result

if __name__ == '__main__':
    app.logger.info("Server is ready for requests.")
    app.run()