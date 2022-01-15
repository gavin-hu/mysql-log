# MySQLog

MySQLog is command line program used to collect mysql slow query log like Porcona Toolkit's pt-query-digest.

``` bash
  -e, --env TEXT                  The environment of mysql log to collect
                                  [default: default]
  -u, --user TEXT                 The user of database for collecting
                                  [required]
  -p, --password TEXT             The password of database for collecting
                                  [required]
  -h, --host TEXT                 The host of database for collecting mysql
                                  log  [default: localhost]
  -P, --port INTEGER              The port of database for collecting mysql
                                  log  [default: 3306]
  -d, --database TEXT             The database for collecting mysql log
                                  [default: test]
  -t, --thread-size INTEGER       The thread size of SlowQueryLogConsumer
                                  [default: 1]
  -s, --since TEXT                Filter mysql log by datatime yyyy-MM-dd
                                  HH:mm:ss
  -T, --query-time FLOAT          Filter mysql log by query_time  [default:
                                  0.3]
  --enable-fingerprint            Enable query sql fingerprint
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
        `env` VARCHAR(64) NOT NULL DEFAULT 'default' comment '环境',
        `datetime` DATETIME NOT NULL comment '执行时间',
        `database` VARCHAR(50) NULL comment '数据库',
        `user`  VARCHAR(50) NULL comment '数据库用户',
        `host` VARCHAR(100) NULL comment '数据库主机',
        `fingerprint` TEXT NULL comment 'SQL指纹',
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
mysqlog -uroot -p123456 -hlocalhost -P3306 -dtest -t2 -T0.5 -s"2021-01-01 00:00:00" mysql-slow.log
```



## FAQ

1. how to enable mysql's slow query log



2. how to know mysql's slow query log file's location