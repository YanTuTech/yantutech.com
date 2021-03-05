class Position:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        # self.output = kwargs['output']
        # self.name = kwargs['name']
        # self.salary = kwargs['salary']
        # self.resp = kwargs['resp']
        # self.req = kwargs['req']
        # self.bonuds = kwargs['bonuds']

class Paritition:
    RESP = 'resp'
    REQ = 'req'
    BONUS = 'bonus'
        
def parse_info(fn):
    with open(fn, 'rb') as f:
        data = f.read().decode('UTF-8')
        lines = data.split('\n')
    
    resp = []
    req = []
    bonus = []
    current = None

    for line in lines:
        if "> 输出名称" in line:
            output = line[7:].strip()
            continue
        if "> 岗位名称" in line:
            name = line[7:].strip()
            continue
        if "> 待遇" in line:
            salary = line[5:].strip()
            continue
        if "> 岗位职责" in line:
            current = Paritition.RESP
            continue
        if "> 职位要求" in line:
            current = Paritition.REQ
            continue
        if "> 加分项" in line:
            current = Paritition.BONUS
            continue
        if current == Paritition.RESP and line.strip() != "":
            resp.append(line.strip())
        if current == Paritition.REQ and line.strip() != "":
            req.append(line.strip())
        if current == Paritition.BONUS and line.strip() != "":
            bonus.append(line.strip())
    print(output, name, salary, resp, req, bonus)
    return Position(
        output=output,
        name=name,
        salary=salary,
        resp=resp,
        req=req,
        bonus=bonus
    )
        

def write_detail(fn):
    template = open('job_detail_template.html', 'rb').read().decode('UTF-8')
    info = parse_info(fn)
    template = template.replace('[岗位名称]', info.name)
    template = template.replace('[待遇]', info.salary)
    if "实习" in info.name:
        template = template.replace('[类型]', "实习")
    else:
        template = template.replace('[类型]', "全职")
    li_template = '<li class="text-secondary">{}</li>'
    resp_content = []
    resp_len = len(info.resp)
    for i in range(resp_len):
        if i < resp_len - 1:
            resp_content.append(li_template.format(info.resp[i] + "；"))
        else:
            resp_content.append(li_template.format(info.resp[i] + "。"))
        
    template = template.replace('[岗位职责]', '\n'.join(resp_content))

    req_content = []
    req_len = len(info.req)
    for i in range(req_len):
        if i < req_len - 1:
            req_content.append(li_template.format(info.req[i] + "；"))
        else:
            req_content.append(li_template.format(info.req[i] + "。"))

    template = template.replace('[职位要求]', '\n'.join(req_content))

    bonus_content = []
    bonus_len = len(info.bonus)
    for i in range(bonus_len):
        if i < bonus_len - 1:
            bonus_content.append(li_template.format(info.bonus[i] + "；"))
        else:
            bonus_content.append(li_template.format(info.bonus[i] + "。"))

    template = template.replace('[加分项]', '\n'.join(bonus_content))

    with open(f'{info.output}.html', 'wb') as f:
        f.write(template.encode('UTF-8'))
    return info

def write_list(info_list):
    template = open('job_list_template.html', 'rb').read().decode('UTF-8')
    div_template = '''
    <div class="job-list-item-box mt-6 mb-6 px-4 py-3 shadow bg-white rounded">
        <a href="[output].html">
            <div class="job-box w-100">
                
                <h3 class="mr-3 my-4">[岗位名称]</h3>
                <p class="mb-3">
                    <span class="mr-2">上海</span>
                    <span class="mr-2">[待遇]</span>
                    <span class="mr-2">[类型]</span>
                </p>
                <ol class="pl-3">
                [岗位职责]
                </ol>
            </div>
        </a>
    </div>
    '''
    li_template = '<li>{}</li>'
    divs = []
    for info in info_list:
        tmp_template = div_template.replace('[output]', info.output)
        tmp_template = tmp_template.replace('[岗位名称]', info.name)
        tmp_template = tmp_template.replace('[待遇]', info.salary)
        tmp_template = tmp_template.replace('[类型]', "实习" if "实习" in info.name else "全职")

        resp_content = []
        resp_len = len(info.resp)
        for i in range(resp_len):
            if i < resp_len - 1:
                resp_content.append(li_template.format(info.resp[i] + "；"))
            else:
                resp_content.append(li_template.format(info.resp[i] + "。"))
            
        tmp_template = tmp_template.replace('[岗位职责]', '\n'.join(resp_content))

        divs.append(tmp_template)
    divs = '\n'.join(divs)
    template = template.replace('[info_list]', divs)
    with open('job_list.html', 'wb') as f:
        f.write(template.encode('UTF-8'))


import os
info_list = []
for f in os.listdir():
    if '.txt' not in f:
        continue
    if f == '招聘信息模板.txt':
        continue
    info = write_detail(f)
    info_list.append(info)

intern_list = []
others_list = []
for info in info_list:
    if '实习' in info.name:
        intern_list.append(info)
    else:
        others_list.append(info)
info_list = intern_list + others_list
write_list(info_list)
