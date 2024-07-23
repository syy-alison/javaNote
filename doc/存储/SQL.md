# 一、操作数据库

## 1.1 操作数据库

## 1.2 数据库列类型

> 数值

- tinyint   十分小的数据    1个字节
- smallint  较小的数据      2个字节
- mediumint  中等大小的数据   3个字节
- **int             标准的整数       4个字节**
- bigint        较大的数据     8个字节
- float         浮点数              4个字节
- double     浮点数              8个字节
- decimal     字符串形式的浮点数    金融计算的时候，一般使用decimal



> 字符串

- char      固定大小的字符串     0-255
- **varchar    可变字符串             0-65535**
- tinytest    微型文本                 2^8-1
- test           文本串                   2^16-1



> 时间和日期

- data    YYYY-MM-DD   日期格式
- time     HH:mm:ss  时间格式
- **datatime    YYYY-MM-DD HH:mm:ss 最常用的时间格式**
- **timestamp   时间戳      1970.1.1到现在的毫秒数**
- year 年份表示



> NULL

- 没有值，未知
- ==注意，不要使用NULL进行运算，结果为NULL

## 1.3 数据库的字段属性

**Unsigned**

- 无符号的整数
- 声明了该列不能声明为负数

**zerofill** 

- 0填充的
- 不足的位数用0填充     int(3)      5---->005

**自增**

- 通常理解为自增，自动在上一条记录的基础上+1(默认)
- 通常用来设计唯一的主键  index,必须是整数类型
- 可以自定义设计主键自增的起始值和步长

**非空  NULL not null**

- 假设设置为not null，如果不给他赋值，就会报错
- NULL，如果不填写值，默认为null

**默认**

- 自定义设置默认的值
- 如果设置sex 默认值为男，则如果不指定该列，则默认值为男

## 1.4 创建数据库表

```mysql
-- 目标：创建一个school数据库
-- 创建学生表(列，字段)
-- 学号int  登陆密码 varchar(20)，姓名，性别 varchar(2) 出生日期(datatime) 家庭住址 email
-- 注意点  使用英文()  表的名称和字段尽量用``括起来
-- AUTO_INCREMENT 自增
-- 字符串使用''括起来，话要加, 最后一个不用加
CREATE TABLE IF NOT EXISTS `student`(
     `id`  INT(4) NOT NULL AUTO_INCREMENT COMMENT '学号',
     `name` VARCHAR(30) NOT NULL DEFAULT '匿名' COMMENT '姓名',
      `pwd`  VARCHAR(20)  NOT NULL DEFAULT '123456' COMMENT '密码',
      `sex`  VARCHAR(2)   NOT NULL DEFAULT '女' COMMENT '性别',
      `birthday` DATETIME  DEFAULT NULL COMMENT '出生日期',
      `address`  VARCHAR(100)    DEFAULT NULL COMMENT '家庭住址',
       `email`  VARCHAR(50)    DEFAULT NULL COMMENT '邮箱',
       PRIMARY KEY(`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
```

格式

```mysql
CREATE TABLE IF NOT EXISTS `表名`(
    
    `字段名` 列类型 [属性] [索引] [注释]，
    `字段名` 列类型 [属性] [索引] [注释]，
    .....
    `字段名` 列类型 [属性] [索引] [注释]，
)[表类型][字符集设置][注释]
```

## 1.5 INNODB与MYISAM的区别

|              | MYISAM | INNODB                 |
| ------------ | ------ | ---------------------- |
| 事务支持     | 不支持 | 支持                   |
| 行锁         | 不支持 | 支持                   |
| 外键约束     | 不支持 | 支持                   |
| 全文索引     | 支持   | 不支持                 |
| 表空间的大小 | 较小   | 较大，约为myisam的两倍 |

常规使用操作：

- MYISAM  节约空间，速度较快
- INNODB 安全性高，支持事务，支持外键就支持多表多用户



> 在物理空间存在的位置

所有数据库文件都存在data目录下

本质还是文件的存储！

MYSQL引擎在物理文件上的区别

- INNODB在数据库表中只有一个*.frm文件，以及上级目录下的ibdata1文件

- MYISAM 对应文件

  - *.frm 表结构的定义文件
  - *.MYD 数据文件（data)

  - *.MYI 索引文件(index)

> 设置数据库表的字符集编码

```
CHARSET=utf8
```

不设置的话，会是mysql默认的字符集编码（不支持中文！）

## 1.6 修改删除表

> 修改表

```mysql
-- 修改表名 ALTER TABLE 旧表名 RENAME AS 新表名
ALTER TABLE teacher RENAME AS teacher1
-- 增加表的字段 ALTER TABLE 表明 ADD 字段名 列属性
ALTER TABLE teacher1 ADD age INT(1)
-- 修改表的字段(重命名，修改约束)
-- ALTER TABLE 表名 MODIFY 字段名 列属性[] 
ALTER TABLE teacher MODIFY age VARCHAR(11)  -- 修改约束
-- ALTER TABLE 表名 CHANGE 旧名字 新名字 列属性[] 
ALTER TABLE teacher CHANGE age age1 INT(1)  -- 字段重命名
-- 删除表的字段 ALTER TABLE 表名 DROP 字段名
ALTER TABLE teacher1 DROP age1
```

> 删除表

```mysql
DROP TABLE IF EXISTS teacher1
```

所有的创建和删除操作尽量加上判断，以免报错~

# 二、MYSQL数据管理

## 2.1外键

> 方式一 :在创建表的时候，增加约束

```mysql
CREATE TABLE IF NOT EXISTS `student`(
     `id`  INT(4) NOT NULL AUTO_INCREMENT COMMENT '学号',
     `name` VARCHAR(30) NOT NULL DEFAULT '匿名' COMMENT '姓名',
      `pwd`  VARCHAR(20)  NOT NULL DEFAULT '123456' COMMENT '密码',
      `sex`  VARCHAR(2)   NOT NULL DEFAULT '女' COMMENT '性别',
      `birthday` DATETIME  DEFAULT NULL COMMENT '出生日期',
      `gradeid`  INT(10) NOT NULL COMMENT '学生的年级'
      `address`  VARCHAR(100)    DEFAULT NULL COMMENT '家庭住址',
       `email`  VARCHAR(50)    DEFAULT NULL COMMENT '邮箱',
       PRIMARY KEY(`id`)  
       KEY `FK_gradeid` (`gradeid`)-- 
       CONSTRAINT `FK_gradeid` FOREIGN KEY(`gradeid`) REFERENCES `grade`(`gradeid`)-- 为grade表的外键
) ENGINE=INNODB DEFAULT CHARSET=utf8
```

删除有外键关系的表的时候，必须要删除引用别人的表（从表），再删除被引用的表。（主表)

> 方式二：创建表的时候没有外键关系

```mysql
ALTER TABLE `student`
ADD CONSTRINT `FK_gradeid` FOREIGN KEY(`gradeid`) REFERENCES `grade`(`gradeid`)
```

以上的操作都是物理外键，数据库级别的外键，不建议使用（避免数据过多造成困扰）

==最佳实践==

- 数据库就是单纯的数据，只用来存数据，只有行（数据）和列（字段）
- 我们想要使用多张表的数据，想使用外键，就用程序来实现。

## 2.2 DML语言

DML语言：数据库操作语言

### 2.2.1 插入

> Insert

```mysql
INSERT INTO 表名([字段名1,字段名2,字段名3]) VALUES('值1'),('值2'),('值3')...
INSERT INTO `grade` (`gradename`)  VALUES (`大二`)，(`大三`)  -- 可以同时插入多条数据，VALUE后面的值，需要使用,隔开
INSERT INTO `student` (`name`,`pwd`,`sex`) VALUES('张三','1234','男') 

```

注意事项：字段和字段使用英文逗号隔开

字段是可以省略的，但是要一一对应。如

```mysql
INSERT INTO `student` VALUES('张三','1234','男')-- 这时候要把所有的都补全
```

### 2.2.2 修改

> update 

```mysql
-- 修改学生名字
UPDATE `student` SET `name` = 'syy' WHERE id=1;

-- 不指定条件的情况下，会改动所有的表
UPDATE `student` SET `name`='长江七号'

-- 修改多个属性，用逗号隔开
UPDATE `student` SET `name`= 'syy',email= '123@163.com' WHERE id=1;

-- 语法
-- UPDATE 表名 set clonum_name=value [,clonum_name=value ]where [条件]
-- clonum_name是数据的列，尽量带上``
-- 条件，筛选的条件，如果没有指定列，将会修改所有的列
-- value 是一个具体的值，也可以是一个变量
UPDATE `student` SET `birthday`= CURRENT_TIME WHERE `name`='长江七号' AND sex='男'
```

条件: where 子句运算符  id等于某个值，大于某个值，在某个区间内修改

| 操作符              | 含义         | 例子                        |
| ------------------- | ------------ | --------------------------- |
| =                   | 等于         | where id=5                  |
| <> 或 !=            | 不等于       | where id<>5                 |
| >                   | 小于         |                             |
| <                   | 大于         |                             |
| <=                  | 小于等于     |                             |
| >=                  | 大于等于     |                             |
| BETWEEN ... and ... | 在某个范围内 | BETWEEN 2 AND 5  含义 [2,5] |
| AND                 | 与           | id>2 AND id<5               |
| OR                  | 或           | id>2 OR id<5                |

### 2.2.3 删除

> delete 

```mysql
-- 删除数据
DELETE FROM `student` WHERE id=1;
```

> Truncate 

作用：完全清空一个数据库表，但是表的结构和索引约束不会变！

```mysql
-- 清空 student表
TRUNCATE TABLE `student`
```

> delete 和 Truncate 区别

- 相同点：都能删除数据，都不会删除表结构
- 不同点
  - TRUNCATE 重新设置自增列，计数器会归零
  - TRUNCATE 不会影响事务 

```mysql
CREATE TABLE `test`(
   `id` INT(4) NOT NULL AUTO_INCREMENT,
    `coll` VARCHAR(20) NOT NULL;
    PRIMARY KEY(`id`)
)ENGINE = INNODB DEFAULT CHARSET=utf8

INSERT INTO `test` (coll`) VALUES ('1'),('2'),('3')

DELETE FROM `test` --不会影响自增  后面插入数据主键从4开始
TRUNCATE TABLE`student` --影响自增，自增会归零  后面插入数据主键从1开始

```

DELETE删除的问题，重启数据库，现象：

- INNODB  自增列会从1开始（存在内存中，断电即失）
- MYISAM 继续从上一个自增量开始（存在文件中，不会丢失）

# 三、DQL查询数据

## 3.1 DQL

(Data Query language)  数据库查询语言

- 所有的查询操作都用它  select

```mysql
SELECT [ALL | DISTINCT]
{*|table.* }
FROM Table_name [as table]
	[left | right |inner join table name2 ON]
	[WHERE ..]
	[GROUP BY...]
	[HAVING..] 
	[ORDER BY..]
	[LIMIT startindex,pagesize]

```



## 3.2 指定查询字段

```mysql
-- 查询全部的学生
SELECT * FROM student
SELECT * FROM result

-- 查询指定字段
SELECT studentNo,studentName FROM student

-- 别名
SELECT studentNo AS 学号，studentName AS 学生姓名 FROM student AS s
 
-- 函数  Concat(a,b)  拼接字符串
SELECT CONCAT('姓名：' StudentName)  AS 新名字 FROM student
```

> 去重 DISTINCT 

```mysql
-- 去除SELECT 查询出来的结果中重复的数据，重复的数据只显示一条
SELECT DISTINCT studentNo FROM result
```

> 数据库的列(表达式)

```mysql
SELECT VERSION() -- 查询系统版本(函数)
SELECT 100*3-1 AS 计算结果  -- 用来计算
SELECT @@auto_increment_increment  --查询自增的步长

-- 学员考试成绩 +1分查看
SELECT studentNo,studentresult+1 AS '提分后' FROM result
```

## 3.3 WHERE条件子句

作用：检测数据中符合条件的值

> 逻辑运算符

| 运算符    | 语法         | 描述   |
| --------- | ------------ | ------ |
| and   &&  | a and b      | 逻辑与 |
| or   \|\| | a or b       | 逻辑或 |
| NOT !     | not a     !a | 非     |

```mysql
-- 查询考试成绩在95-100分
SELECT studentNo,studentResult FROM result
WHERE studentResult>=95  AND dentResult<=100
-- 模糊查询 区间
SELECT studentNo,studentResult FROM result
WHERE studentResult BETWEEN 95 AND 100

-- 除了10000号学生之外的同学的成绩  !=  NOT
SELECT studentNo,studentResult FROM result
WHERE NOT studentNo=1000
```

> 模糊查询：比较运算符

| 运算符      | 语法               | 描述                                 |
| ----------- | ------------------ | ------------------------------------ |
| IS NULL     | a is null          | 如果操作符为NULL  结果为真           |
| IS NOT NULL | a is not null      | 如果操作符不为null，结果为真         |
| BETWEEN     | a between b and  c | 若a在b和c之间，结果为真              |
| Like        | a like b           | SQL匹配，如果a匹配b ,则结果为真      |
| In          | a in(a1,a2,a3...)  | 假设a 在a1,a2,a3中的一个，则返回为真 |

```mysql
-- =============like========
-- 查询姓刘的同学
-- like 结合%(代表0到任意个字符)  _(一个字符)
SELECT studentNo,studentName  From  student
WHERE studentName LIKE '刘%'
-- 查询姓刘的同学，名字后面只有一个字
SELECT studentNo,studentName  From  student
WHERE studentName LIKE '刘_'
-- 查询姓刘的同学，名字后面只有两个字
SELECT studentNo,studentName  From  student
WHERE studentName LIKE '刘__'

-- 查询名字中带有嘉的
SELECT studentNo,studentName  From  student
WHERE studentName LIKE '%嘉%'

-- ==========in(具体的一个或者多个值)======
-- 查询1001，1002，1003号学员
SELECT studentNo,studentName FROM student
WHERE studentNo in(1001,1002,1003)
-- 查询在北京的学生
SELECT studentNo,studentName FROM student
WHERE Adress in('安徽','河南');

-- ==========null not null======
-- 查询地址为空的学生  null
SELECT studentNo,studentName FROM student
WHERE address='' OR adress is NULL

-- 查询有出生日期的同学
SELECT studentNo,studentName FROM student
WHERE bornDate is Not NULL

```

## 3.4 联表查询

> JOIN

![img](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpic2.zhimg.com%2Fv2-9558e847d122f104dc9acb19e600496d_b.jpg&refer=http%3A%2F%2Fpic2.zhimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1621134684&t=49a6b78deb38980ef8ccd1d2951528bf)

**1. 内连接 (INNER JOIN)**内连接返回两个表中有匹配关系的行。**示例**: 这个查询返回每个员工及其所在的部门名称。

```sql
SELECT employees.name, departments.name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;
```



```mysql
--  ======== 联表查询=====
-- 查询参加了考试的同学(学号，姓名，科目编号，分数)
/*思路
1.分析需求，分析查询的字段来自哪些表(连接查询)
2. 确定使用哪种连接查询
确定交叉点(这两个表中哪些数据是相同的)。
判断条件：学生表中的studentNo=成绩表 studentNo
*/

-- Inner Join  如果表中至少有一个匹配，就返回行,两个表共有的部门
SELECT s.studentNo,studentName,subjectNo,studentResult
FROM student s
INNER JOIN result r
ON s.studentNo=r.studentNo

-- right join  会从右表中返回所有的值，即使左表没有匹配的值,左表没有匹配就为null
SELECT s.studentNo,studentName,subjectNo,studentResult
FROM student s
Right JOIN result r
ON s.studentNo=r.studentNo

-- left join  会从左表中返回所有的值，即使右表没有匹配的值,右表没有匹配就为null

SELECT s.studentNo,studentName,subjectNo,studentResult
FROM student s
left JOIN result r
ON s.studentNo=r.studentNo

-- 查询缺考的同学
SELECT s.studentNo,studentName,subjectNo,studentResult
FROM student s
left JOIN result r
ON s.studentNo=r.studentNo
WHERE studentResult IS NULL

-- 查询了参加考试的同学信息：学号，学生姓名，科目名，分数
/*思路：
1.分析需求，分析查询的字段来自哪些表，student(学号，学生姓名),result(学号，科目编号，分数),subject(科目编号，科目名)
*/
SELECT s.studentNo,studentName,subjectName,sudentResult
FROM student s
RIGHT JOIN result r
ON r.studentNo=s.studentNo
INNER JOIN subject sub
ON r.subjectNo= sub.subjectNo

-- 查询了参加数据库考试的同学信息：学号，学生姓名，科目名，分数
SELECT s.studentNo,studentName,subjectName,sudentResult
FROM student s
RIGHT JOIN result r
ON r.studentNo=s.studentNo
INNER JOIN subject sub
ON r.subjectNo= sub.subjectNo
WHERE subjectName='数据库'
```

> 自连接

自己的表和自己的表连接，核心：一张表拆为两个一样的表即可

## 3.5 分页和排序

> ORDER BY     LIMIT

```mysql
-- 排序 升序ASC  降序DESC
SELECT s.studentNo,studentName,subjectName,sudentResult
FROM student s
RIGHT JOIN result r
ON r.studentNo=s.studentNo
INNER JOIN subject sub
ON r.subjectNo= sub.subjectNo
WHERE subjectName='数据库'
ORDER　BY　sudentResult　DESC

-- 分页 LIMIT  所有语句的最后一句
-- 为什么要分页  缓解数据库压力
-- Limit 起始页 页的大小。、
-- 显示第n页： Limit (n-1)*pageSize, pageSize
-- Limit 0,5  1-5的数据
-- Limit 1,5  2-6的数据

SELECT s.studentNo,studentName,subjectName,sudentResult
FROM student s
RIGHT JOIN result r
ON r.studentNo=s.studentNo
INNER JOIN subject sub
ON r.subjectNo= sub.subjectNo
WHERE subjectName='数据库'
ORDER　BY　sudentResult　DESC
LIMIT 0,5
```

## 3.6 子查询

```mysql
-- 查询数据结构的所有考试结果(学号，科目编号，成绩)，降序排列
-- 方式一：使用连接查询
SELECT StudentNo,r.subjectNo,studentResult
FROM result r
INNER JOIN subject sub
ON r.StudentNo = sub.StudentNo
WHERE SubjectName= '数据结构'
ORDER　BY　sudentResult　DESC
-- 方式2 使用子查询
SELECT studentNo,subjectNo,studentResult
FROM result
WHERE subjectNo=(
     SELECT subjectNo From subject
     WHERE SubjectName ='数据结构'
)
ORDER BY studentResult DESC

-- 分数不少于80分的学生的学号和姓名
SELECT studentNo,studentName
FROM student s
INNER JOIN result r
ON r.StudentNo = s.StudentNo
WHERE StudentResult>=80

-- 在这个基础上增加一个科目 高等数学分数不少于80分的学生的学号和姓名
-- 使用子查询
SELECT DISTINCT studentNo,studentName
FROM student s
INNER JOIN result r
ON r.StudentNo = s.StudentNo
WHERE StudentResult>=80 AND SubjectNo=(
    SELECT SubjectNo FROM subject
    WHERE subjectName='高等数学'
)
-- 方法2 联表查询
SELECT DISTINCT s.studentNo,StudentName
FROM student s
INNER JOIN result r
ON s.studentNo = r.studentNo
INNER JOIN subject sub
ON r.subjectNo = sub.subjectNo
WHERE subjectName='高等数学' AND studentResult>=80

-- 方法3 
SELECT studentNo,StudentName FROM student WHERE StudentNo IN(
	SELECT StudentNo FROM result WHERE studentResult>80 AND subjectNo=(
    	SELECT subjectNo FROM subject WHERE subjectName='高等数学'
    )
)

```

# 四、MYSQL函数

## 4.1 常用函数

```mysql
-- 数学运算(不用记)
SELECT ABS(-8)  -- 绝对值
SELECT CEILING(9,4) -- 向上取整
SELECT FLOOR(9,4) -- 向下取整
SELECT RAND()  -- 返回一个0到1的随机数
SELECT SIGN(-1)  -- 判断一个数的符号，负数返回-1，整数返回1
-- 字符串函数(不用记)
SELECT CHAR_LENGTH('syy') -- 字符串长度
SELECT CONCAT('s','y','y') -- 拼接字符串
SELECT INSERT('suyuying',1,2,'syy') -- 查询，从某个位置开始替换某个长度 从s开始，将su改为syy.即syyyuying
SELECT LOWER('SYY')  -- 转为小写
SELECT UPPER('syy')  -- 转为大写
SELECT INSTR('syy',h) -- 返回第一次出现的子串的索引
SELECT REPLACE('syy','s','y') -- 替换指定的字符串
-- 时间和日期(要记)
SELECT CURRENT_DATE() -- 获取当前的日期
SELECT CURDATE()  -- 获取当前日期
SELECT NOW()   -- 获取当前时间
SELECT LOCALTIME()   -- 本地时间
SELECT SYSTIME()   -- 系统时间
SUM(if(name = 'syy',1,0))  -- 如果name=syy则为1,统计name=syy的个数
ifnull(sum(quantity), 0)  --如果 sum(quantity)为空，则等于0
```



## 4.2 聚合函数

| 函数名称 | 描述   |
| -------- | ------ |
| COUNT()  | 计数   |
| SUM()    | 求和   |
| AVG()    | 平均值 |
| MAX()    | 最大值 |
| MIN()    | 最小值 |

```mysql
-- 聚合函数
SELECT COUNT(studentname) FROM student; -- 指定列,会忽略所有的NULL值
SELECT COUNT(*) FROM student; -- count(*)  不会忽略null值
SELECT COUNT(1) FROM student;  -- count(1)  不会忽略null值

SELECT SUM(studentResult) AS 总和 FROM result
SELECT AVG(studentResult) AS 平均分 FROM result
SELECT MAX(studentResult) AS 最高分 FROM result
SELECT MIN(studentResult) AS 最低分 FROM result


```



## 4.3 分组和过滤

```mysql
SELECT subjectName,AVG(studentResult) AS 平均分,MAX(studentResult),MIN(studentResult)
FROM result r 
INNOR JOIN subject sub
ON r.subjectNo=sub.subjectNo
GROUP BY r.subjectNo   -- 分组
HAVING 平均分>80
```

# 五、事务

==要么都成功，要么都失败==

> 事务原则：ACID 原则   原子性，一致性，隔离性，持久性

- 原子性

要么都成功，要么都失败

- 一致性

事务前后的数据完整性要保证一致

- 持久性

事务一旦提交则不可逆，被持久化到数据库中。

- 隔离性

事务的隔离性是指多个用户并发访问数据库时，数据库为每个用户开启的事务，不能被其他事务的操作的数据所干扰。

> 隔离产生的问题

- 脏读：一个事务读取了另一个事务未提交的数据
- 不可重复读：在一个事务内读取表中的某一行数据，多次读取结果不同。
- 虚读：指在一个事务中读到了别的事务插入的数据，导致前后读取不一致。

```mysql
-- mysql是默认开启事务自动提交的
SET autocommit= 0 -- 关闭
SET autocommit= 1 -- 开启

-- 手动处理事务 
SET autocommit= 0 -- 关闭
-- 事务开启
START TRANSANCTION 

INSERT xxx
INSERT xxx

-- 提交：持久化(成功)
COMMIT
-- 回滚(回到原来的样子)
ROLLBACK
-- 恢复默认提交
SET autocommit= 1 -- 开启
```



