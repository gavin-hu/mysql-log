CREATE TABLE `mysql_slow_query_log` (
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