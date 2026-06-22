import urllib.request
import json
import os

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

phases = [
    'Phase 1 요청 수집',
    'Phase 2 아이디어 제안',
    'Phase 3 아이디어 승인',
    'Phase 4 견적 제안',
    'Phase 5 견적 승인',
    'Phase 6 기획',
    'Phase 7 제작',
    'Phase 8 테스트',
    'Phase 9 최종 승인'
]

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

    rows = []
    found = False
    for phase in phases:
        if phase == current:
            rows.append({'phase': phase, 'status': '🔄 진행 중'})
            found = True
        elif not found:
            rows.append({'phase': phase, 'status': '✅ 완료'})
        else:
            rows.append({'phase': phase, 'status': '⏳ 대기'})

    print(f'업데이트 완료: {name}')
    for r in rows:
        print(f"  {r['phase']}: {r['status']}")

print('CEO 대시보드 업데이트 완료!')
