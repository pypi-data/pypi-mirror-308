from datetime import datetime, timedelta
import requests
from flask import request
from llama_index.core.tools import FunctionTool

app_server_url = "http://127.0.0.1:8080/business/data"

def contract_sum(begin: str, end: str) -> str:
    """通过年份获取合同金额"""
    userId = request.get_json()['userId']
    print(f"userid:{userId}")
    url = f"{app_server_url}/getContractAmountSum?startTime={begin}&endTime={end}&userId={userId}"
    print(url)
    resp = requests.get(url)
    print(resp.status_code)
    print(resp.json())
    return resp.json()


def current_year(begin: str) -> str:
    print("param begin:" + begin)
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year + 1, 1, 1) - timedelta(days=1)
    return start_of_year.strftime("%Y-%m-%d") + "," + end_of_year.strftime("%Y-%m-%d")

contract_sum = FunctionTool.from_defaults(fn=contract_sum)

current_year = FunctionTool.from_defaults(fn=current_year)


def function_tool_list():
    return [contract_sum, current_year]




