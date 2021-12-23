import re


import re

s = "Example String"
replaced = re.sub("[ES]", "a", s)
print(replaced)

output = re.sub(
    "set\s+timestamp=\d+;\s+",
    "",
    "set timestamp=123131231; insert into xxl_job_log ( `job_group`, `job_id`, `trigger_time`, `trigger_code`, `handle_code` ) values(?+);",
)


print(output)
