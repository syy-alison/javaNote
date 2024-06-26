### Mybatis是什么？

MyBatis 是一个流行的 Java 持久层框架，它提供了简单的 API 和灵活的配置，用于将 Java 对象映射到关系型数据库的记录。MyBatis 允许开发者通过 XML 或注解来配置 SQL 语句，从而实现对数据库的操作，包括插入、查询、更新和删除等。

MyBatis 的主要特点包括：

1. **SQL 映射**：MyBatis 允许开发者通过 XML 或注解来编写 SQL 语句，并将这些语句映射到 Java 方法上。
2. **动态 SQL**：MyBatis 支持动态 SQL，可以根据条件生成不同的 SQL 语句。
3. **事务管理**：MyBatis 支持声明式事务管理，可以与 Spring 框架集成，实现更高级的事务控制。
4. **缓存机制**：MyBatis 提供了一级缓存和二级缓存，可以减少数据库访问次数，提高性能。
5. **映射器接口**：MyBatis 允许开发者定义映射器接口，而不需要实现它们，MyBatis 会在运行时动态生成实现。
6. **插件系统**：MyBatis 提供了插件接口，开发者可以编写自己的插件来扩展 MyBatis 的功能。

MyBatis 通常用于需要高度定制 SQL 语句的应用程序中，它提供了比传统的 ORM（对象关系映射）框架如 Hibernate 更多的灵活性。然而，MyBatis 也要求开发者编写更多的 SQL 代码，这可能会增加项目的复杂性。

### #{} 和 ${} 的区别是什么？

答：

- `${}`是 Properties 文件中的变量占位符，它可以用于标签属性值和 sql 内部，属于原样文本替换，可以替换任意内容，比如${driver}会被原样替换为`com.mysql.jdbc. Driver`。

一个示例：根据参数按任意字段排序：

```sql
select * from users order by ${orderCols}
```

`orderCols`可以是 `name`、`name desc`、`name,sex asc`等，实现灵活的排序。

- `#{}`是 sql 的参数占位符，MyBatis 会将 sql 中的`#{}`替换为? 号，在 sql 执行前会使用 PreparedStatement 的参数设置方法，按序给 sql 的? 号占位符设置参数值，比如 ps.setInt(0, parameterValue)，`#{item.name}` 的取值方式为使用反射从参数对象中获取 item 对象的 name 属性值，相当于 `param.getItem().getName()`。

### xml 映射文件中，除了常见的 select、insert、update、delete 标签之外，还有哪些标签？

注：这道题是京东面试官面试我时问的。

答：还有很多其他的标签， `<resultMap>`、 `<parameterMap>`、 `<sql>`、 `<include>`、 `<selectKey>` ，加上动态 sql 的 9 个标签， `trim|where|set|foreach|if|choose|when|otherwise|bind` 等，其中 `<sql>` 为 sql 片段标签，通过 `<include>` 标签引入 sql 片段， `<selectKey>` 为不支持自增的主键生成策略标签。

### Dao 接口的工作原理是什么？Dao 接口里的方法，参数不同时，方法能重载吗？

最佳实践中，通常一个 xml 映射文件，都会写一个 Dao 接口与之对应。Dao 接口就是人们常说的 `Mapper` 接口，接口的全限名，就是映射文件中的 namespace 的值，接口的方法名，就是映射文件中 `MappedStatement` 的 id 值，接口方法内的参数，就是传递给 sql 的参数。 `Mapper` 接口是没有实现类的，当调用接口方法时，接口全限名+方法名拼接字符串作为 key 值，可唯一定位一个 `MappedStatement` ，举例：`com.mybatis3.mappers. StudentDao.findStudentById` ，可以唯一找到 namespace 为 `com.mybatis3.mappers. StudentDao` 下面 `id = findStudentById` 的 `MappedStatement` 。在 MyBatis 中，每一个 `<select>`、 `<insert>`、 `<update>`、 `<delete>` 标签，都会被解析为一个 `MappedStatement` 对象。

### 简述 MyBatis 的 xml 映射文件和 MyBatis 内部数据结构之间的映射关系？

MyBatis 将所有 xml 配置信息都封装到 All-In-One 重量级对象 Configuration 内部。在 xml 映射文件中， `<parameterMap>` 标签会被解析为 `ParameterMap` 对象，其每个子元素会被解析为 ParameterMapping 对象。 `<resultMap>` 标签会被解析为 `ResultMap` 对象，其每个子元素会被解析为 `ResultMapping` 对象。每一个 `<select>、<insert>、<update>、<delete>` 标签均会被解析为 `MappedStatement` 对象，标签内的 sql 会被解析为 BoundSql 对象。

### 为什么说 MyBatis 是半自动 ORM 映射工具？它与全自动的区别在哪里？

答：Hibernate 属于全自动 ORM 映射工具，使用 Hibernate 查询关联对象或者关联集合对象时，可以根据对象关系模型直接获取，所以它是全自动的。而 MyBatis 在查询关联对象或关联集合对象时，需要手动编写 sql 来完成，所以，称之为半自动 ORM 映射工具。

