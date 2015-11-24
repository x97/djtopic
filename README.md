# djtopic

## 话题

###创建
    url : /api/topic/create

### 查看/修改/删除
    url : /api/topic/(?P<pk>[0-9]+)/

    get put delete

### 列表
* url : /api/topic/list
* 参数    status/user_id
         status:
         * ('0', '草稿'),
         * ('1', '发布'),
         * ('2', '隐藏'),
         * ('3', '屏蔽'),
* 示例 :
        获得自己发布的话题：
            /api/topic/list/
        获得别人发布的话题
            /api/topic/list/?user_id=1
        获得主键位1的用户的话题列表
            只能获得某一位用户发布的话题
        获得自己草稿列表
            /api/topic/list/?status=0
        获得自己屏蔽话题列表
            /api/topic/list/?status=3
           不支持获得隐藏话题

### 收藏话题
    url : /api/topic/collection/create/

### 收藏话题列表

    url : /api/topic/collection/list/

### 点赞话题
    url : /api/topic/star/create/

### 点赞话题列表
    url : /api/topic/star/list/

## 评论

### 评论创建
    url : /api/topic/comment/create/

### 回复评论
    url : /api/topic/comment/review/

### 评论列表
* url: /api/topic/comment/list/
* 可选参数 id
* 示例：
        /api/topic/comment/list/
            返回自己发布的所有评论
        /api/topic/comment/list/?id=
            返回某篇话题的所有评论
