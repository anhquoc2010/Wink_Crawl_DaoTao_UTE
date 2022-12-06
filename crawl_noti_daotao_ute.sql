CREATE DATABASE crawl_noti_daotao_ute;
USE crawl_noti_daotao_ute;
CREATE TABLE notification(
    id int(40) not null,
    title longtext CHARSET utf8,
    content longtext CHARSET utf8,
    primary key(id)
);