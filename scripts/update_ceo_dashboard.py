import urllib.request
import json
import os
from datetime import datetime

token = os.environ['NOTION_API_KEY']
headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

def notion_request(url, method='GET', data=None):
    req = urllib.request.Request(
        url,
        method=method,
        data=json.dumps(data or {}).encode(),
        headers=headers
    )
    return json.loads(urllib.request.urlopen(req).read())

# 프로젝트 DB에서 현재 단계 읽기
db_id = '4b69faa56c49485f83e37c734b2061cf'
res = notion_request(
    f'https://api.notion.com/v1/databases/{db_id}/query',
    method='POST'
)

for page in res.get('results', []):
    props = page.get('properties', {})
    title_list = props.get('프로젝트명', {}).get('title', [])
    name = title_list[0].get('plain_text', '') if title_list else ''
    stage_obj = props.get('현재 단계', {}).get('select') or {}
    current = stage_obj.get('name', '')

    if not name or not current:
        continue

    print(f'{name} -> {current}')

    # CEO 대시보드 페이지에 텍스트 추가
    dashboard_id = '387d36b7213481e0b414d8590f9aff31'
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    update_data = {
        'children': [
            {
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': f'[자동업데이트] {now} | {name} | 현재: {current}'
                        }
                    }]
                }
            }
        ]
    }

    notion_request(
        f'https://api.notion.com/v1/blocks/{dashboard_id}/children',
        method='PATCH',
        data=update_data
    )

    print(f'✅ {name} 업데이트 완료!')
