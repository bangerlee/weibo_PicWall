ALTER TABLE pics ADD COLUMN `status` TINYINT NOT NULL DEFAULT 1 COMMENT '1：正常；0：删除';

CREATE TABLE `users` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `u_name` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '用户名',
  `pwd` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '密码',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `status` TINYINT(4) NOT NULL DEFAULT '0' COMMENT '状态 0:停止,1:正常',
  `email` VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`),
  KEY `email` (`email`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

ALTER TABLE `pics` CHANGE `create_date` `create_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '微博发布时间';

INSERT INTO `users` (`u_name`, `pwd`, `email`, `status`) VALUES ('111', '11557649c6a954d548f7dd0963cbecaa', '111@1.cn', 1);

#After 2012-07-01 run these sqls below
ALTER TABLE pics ADD height INT NOT NULL DEFAULT '0' COMMENT '图片高度';
ALTER TABLE pics ADD width INT NOT NULL DEFAULT '0' COMMENT '图片宽度';
ALTER TABLE pics ADD comments INT NOT NULL DEFAULT '0' COMMENT '评论数';
ALTER TABLE pics ADD views INT NOT NULL DEFAULT '0' COMMENT '浏览数';
ALTER TABLE pics ADD likes INT NOT NULL DEFAULT '0' COMMENT 'like数';

#After 2012-07-28 run these sqls below
CREATE TABLE `black_list` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `value` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '黑名单内容',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `type` TINYINT(4) NOT NULL DEFAULT '1' COMMENT '类型 0:UID,1:keyword',
  PRIMARY KEY (`id`),
  KEY `value` (`value`)
) ENGINE=MYISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT '黑名单';

#After 2012-08-07 run these sqls below
CREATE TABLE `comments`(
  `id` BIGINT(20) UNSIGNED NOT NULL COMMENT '评论ID',
  `p_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '图片ID',
  `text` VARCHAR(512) NOT NULL COMMENT '评论内容',
  `user_id` BIGINT(20) NOT NULL COMMENT '发表评论用户ID',
  `mid` BIGINT(20) NOT NULL COMMENT 'mid',
  `user_name` VARCHAR(64) NOT NULL COMMENT '发表评论用户昵称',
  `create_date` TIMESTAMP NULL COMMENT '评论时间',
  PRIMARY KEY (`id`),
  KEY `p_id` (`p_id`),
 KEY `create_date` (`create_date`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TABLE `tmp_comments`(
  `id` BIGINT(20) UNSIGNED NOT NULL COMMENT '评论ID',
  `p_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '图片ID',
  `text` VARCHAR(512) NOT NULL COMMENT '评论内容',
  `user_id` BIGINT(20) NOT NULL COMMENT '发表评论用户ID',
  `mid` BIGINT(20) NOT NULL COMMENT 'mid',
  `user_name` VARCHAR(64) NOT NULL COMMENT '发表评论用户昵称',
  `create_date` TIMESTAMP NULL COMMENT '评论时间',
  PRIMARY KEY (`id`),
 KEY `create_date` (`create_date`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

#After 2012-08-23 run these sqls below
CREATE TABLE `options`(
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `key` VARCHAR(50) NOT NULL COMMENT 'key',
  `value` TEXT NOT NULL COMMENT 'value',
  `create_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_date` TIMESTAMP NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `create_date` (`create_date`)
) ENGINE=MYISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT '配置';