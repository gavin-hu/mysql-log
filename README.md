# MySQLog

MySQLog is command line program used to collect mysql slow query log like Porcona Toolkit's pt-query-digest.

``` bash
Usage: mysqlog [OPTIONS] LOGPATH

Arguments:
  LOGPATH  [required]

Options:
  -e, --env TEXT                  [default: default]
  -u, --user TEXT                 [required]
  -p, --password TEXT             [required]
  -h, --host TEXT                 [default: localhost]
  -P, --port INTEGER              [default: 3306]
  -d, --database TEXT             [default: test]
  -t, --thread-size INTEGER       [default: 1]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
## Install

``` bash
# create python virtual environment for mysqlog
python3 -m venv  mysqlog.venv
# active virtual environment mysqlog.venv 
source mysqlog.venv/bin/activate
# use pip command install mysqlog
pip install mysqlog
# check mysqlog is installed
mysqlog --help
```

## Usage

1. Example log file (mysql-slow.log)

```
# Time: 2020-09-25T06:05:23.747686Z
# User@Host: root[root] @  [10.190.66.171]  Id:     7
# Query_time: 4.412855  Lock_time: 0.000136 Rows_sent: 3  Rows_examined: 8720446
SET timestamp=1601013923;
SELECT id FROM `xxl_job_log`
                WHERE !(
                        (trigger_code in (0, 200) and handle_code = 0)
                        OR
                        (handle_code = 200)
                )
                AND `alarm_status` = 0
                ORDER BY id ASC;
```

2. Init Database

``` bash
# connect to mysql
mysql -uroot -p123456
# create database and use it
mysql> create database test;
mysql> use database test;
# create mysql_slow_query_log table
mysql> CREATE TABLE `mysql_slow_query_log` (
        `id` int NOT NULL auto_increment,
        `md5` VARCHAR(64) NOT NULL comment 'md5',
        `datetime` DATETIME NOT NULL comment '执行时间',
        `database` VARCHAR(50) NULL comment '数据库',
        `user`  VARCHAR(50) NULL comment '数据库用户',
        `host` VARCHAR(100) NULL comment '数据库主机',
        `query` TEXT NOT NULL comment '执行语句',
        `query_time` FLOAT DEFAULT NULL comment '执行时间',
        `lock_time` FLOAT DEFAULT NULL comment '锁定时间',
        `rows_examined` INT DEFAULT NULL comment '扫描总行数',
        `rows_sent` INT DEFAULT NULL comment '返回总行数',
        `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        UNIQUE KEY (`md5`)
      );
# make sure mysql_slow_query_log table is created
mysql> show tables;

```
3. Run MySQLog

``` bash
mysqlog -uroot -p123456 -hlocalhost -dtest mysql-slow.log
```



## FAQ

1. how to enable mysql's slow query log



2. how to know mysql's slow query log file's location