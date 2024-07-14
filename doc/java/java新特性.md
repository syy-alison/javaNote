# Java8

## Interface

- interface 的设计初衷是面向抽象，提高扩展性。这也留有一点遗憾，Interface 修改的时候，实现它的类也必须跟着改。
- 为了解决接口的修改与现有的实现不兼容的问题。新 interface 的方法可以用`default` 或 `static`修饰，这样就可以有方法体，实现类也不必重写此方法。
- 一个 interface 中可以有多个方法被它们修饰，这 2 个修饰符的区别主要也是普通方法和静态方法的区别。
  1. `default`修饰的方法，是普通实例方法，可以用`this`调用，可以被子类继承、重写。
  2. `static`修饰的方法，使用上和一般类静态方法一样。但它不能被子类继承，只能用`Interface`调用。
- interface 新增`default`和`static`修饰的方法，为了解决接口的修改与现有的实现不兼容的问题，并不是为了要替代`abstract class`。在使用上，该用 abstract class 的地方还是要用 abstract class，不要因为 interface 的新特性而将之替换。
  - 接口多实现，类单继承

```java
public interface InterfaceNew {
    static void sm() {
        System.out.println("interface提供的方式实现");
    }
    static void sm2() {
        System.out.println("interface提供的方式实现");
    }

    default void def() {
        System.out.println("interface default方法");
    }
    default void def2() {
        System.out.println("interface default2方法");
    }
    //须要实现类重写
    void f();
}

public interface InterfaceNew1 {
    default void def() {
        System.out.println("InterfaceNew1 default方法");
    }
}

```

```java
public class InterfaceNewImpl implements InterfaceNew , InterfaceNew1{
    public static void main(String[] args) {
        InterfaceNewImpl interfaceNew = new InterfaceNewImpl();
        interfaceNew.def();
    }

    @Override
    public void def() {
        InterfaceNew1.super.def();
    }

    @Override
    public void f() {
    }
}

```

## Lambda 表达式

它是推动 Java 8 发布的最重要新特性。是继泛型(`Generics`)和注解(`Annotation`)以来最大的变化。

使用 Lambda 表达式可以使代码变的更加简洁紧凑。让 java 也能支持简单的*函数式编程*。

语法

```java
(parameters) -> expression 或
(parameters) ->{ statements; }

```

过去给方法传动态参数的唯一方法是使用内部类。比如

```java
@FunctionalInterface
public interface Comparator<T>{}

@FunctionalInterface
public interface Runnable{}

```

```java
new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("The runable now is using!");
            }
}).start();
//用lambda
new Thread(() -> System.out.println("It's a lambda function!")).start();

```

我们发现这些匿名内部类只重写了接口的一个方法，当然也只有一个方法须要重写。这就是我们上文提到的**函数式接口**，也就是说只要方法的参数是函数式接口都可以用 Lambda 表达式。

```java
@FunctionalInterface
public interface LambdaInterface {
 void f();
}
//使用
public class LambdaClass {
    public static void forEg() {
        lambdaInterfaceDemo(()-> System.out.println("自定义函数式接口"));
    }
    //函数式接口参数
    static void lambdaInterfaceDemo(LambdaInterface i){
        i.f();
    }
}

```

## Stream

java 新增了 `java.util.stream` 包，它和之前的流大同小异。之前接触最多的是资源流，比如`java.io.FileInputStream`，通过流把文件从一个地方输入到另一个地方，它只是内容搬运工，对文件内容不做任何*CRUD*。

`Stream`依然不存储数据，不同的是它可以检索(Retrieve)和逻辑处理集合数据、包括筛选、排序、统计、计数等。可以想象成是 Sql 语句。

它的源数据可以是 `Collection`、`Array` 等。由于它的方法参数都是函数式接口类型，所以一般和 Lambda 配合使用。

```java
@Test
public void test() {
  List<String> strings = Arrays.asList("abc", "def", "gkh", "abc");
    //返回符合条件的stream
    Stream<String> stringStream = strings.stream().filter(s -> "abc".equals(s));
    //计算流符合条件的流的数量
    long count = stringStream.count();

    //forEach遍历->打印元素
    strings.stream().forEach(System.out::println);

    //limit 获取到1个元素的stream
    Stream<String> limit = strings.stream().limit(1);
    //toArray 比如我们想看这个limitStream里面是什么，比如转换成String[],比如循环
    String[] array = limit.toArray(String[]::new);

    //map 对每个元素进行操作返回新流
    Stream<String> map = strings.stream().map(s -> s + "22");

    //sorted 排序并打印
    strings.stream().sorted().forEach(System.out::println);

    //Collectors collect 把abc放入容器中
    List<String> collect = strings.stream().filter(string -> "abc".equals(string)).collect(Collectors.toList());
    //把list转为string，各元素用，号隔开
    String mergedString = strings.stream().filter(string -> !string.isEmpty()).collect(Collectors.joining(","));

    //对数组的统计，比如用
    List<Integer> number = Arrays.asList(1, 2, 5, 4);

    IntSummaryStatistics statistics = number.stream().mapToInt((x) -> x).summaryStatistics();
    System.out.println("列表中最大的数 : "+statistics.getMax());
    System.out.println("列表中最小的数 : "+statistics.getMin());
    System.out.println("平均数 : "+statistics.getAverage());
    System.out.println("所有数之和 : "+statistics.getSum());

    //concat 合并流
    List<String> strings2 = Arrays.asList("xyz", "jqx");
    Stream.concat(strings2.stream(),strings.stream()).count();

    //注意 一个Stream只能操作一次，不能断开，否则会报错。
    Stream stream = strings.stream();
    //第一次使用
    stream.limit(2);
    //第二次使用
    stream.forEach(System.out::println);
    //报错 java.lang.IllegalStateException: stream has already been operated upon or closed

    //但是可以这样, 连续使用
    stream.limit(2).forEach(System.out::println);
}

```

## Optional

> 防止 NPE，是程序员的基本修养，注意 NPE 产生的场景：
>
> 1） 返回类型为基本数据类型，return 包装数据类型的对象时，自动拆箱有可能产生 NPE。
>
> 反例：public int f() { return Integer 对象}， 如果为 null，自动解箱抛 NPE。
>
> 2） 数据库的查询结果可能为 null。
>
> 3） 集合里的元素即使 isNotEmpty，取出的数据元素也可能为 null。
>
> 4） 远程调用返回对象时，一律要求进行空指针判断，防止 NPE。
>
> 5） 对于 Session 中获取的数据，建议进行 NPE 检查，避免空指针。
>
> 6） 级联调用 obj.getA().getB().getC()；一连串调用，易产生 NPE。
>
> 正例：使用 JDK8 的 Optional 类来防止 NPE 问题。

假设有一个 `Zoo` 类，里面有个属性 `Dog`，需求要获取 `Dog` 的 `age`。

```java
class Zoo {
   private Dog dog;
}

class Dog {
   private int age;
}

```

传统解决 NPE 的办法如下：

```java
Zoo zoo = getZoo();
if(zoo != null){
   Dog dog = zoo.getDog();
   if(dog != null){
      int age = dog.getAge();
      System.out.println(age);
   }
}

```

`Optional` 是这样的实现的：

```java
Optional.ofNullable(zoo).map(o -> o.getDog()).map(d -> d.getAge()).ifPresent(age ->
    System.out.println(age)
);

```

`ofNullable` 方法和`of`方法唯一区别就是当 value 为 null 时，`ofNullable` 返回的是`EMPTY`，of 会抛出 `NullPointerException` 异常。如果需要把 `NullPointerException` 暴漏出来就用 `of`，否则就用 `ofNullable`。

## Date-Time API

这是对`java.util.Date`强有力的补充，解决了 Date 类的大部分痛点：

1. 非线程安全
2. 时区处理麻烦
3. 各种格式化、和时间计算繁琐
4. 设计有缺陷，Date 类同时包含日期和时间；还有一个 java.sql.Date，容易混淆。

我们从常用的时间实例来对比 java.util.Date 和新 Date 有什么区别。用`java.util.Date`的代码该改改了。

`java.util.Date` 既包含日期又包含时间，而 `java.time` 把它们进行了分离

```java
LocalDateTime.class //日期+时间 format: yyyy-MM-ddTHH:mm:ss.SSS
LocalDate.class //日期 format: yyyy-MM-dd
LocalTime.class //时间 format: HH:mm:ss

```

# Java 11

## String 增强

Java 11 增加了一系列的字符串处理方法：

```java
//判断字符串是否为空
" ".isBlank();//true
//去除字符串首尾空格
" Java ".strip();// "Java"
//去除字符串首部空格
" Java ".stripLeading();   // "Java "
//去除字符串尾部空格
" Java ".stripTrailing();  // " Java"
//重复字符串多少次
"Java".repeat(3);             // "JavaJavaJava"
//返回由行终止符分隔的字符串集合。
"A\nB\nC".lines().count();    // 3
"A\nB\nC".lines().collect(Collectors.toList());

```

## Optional 增强

新增了`isEmpty()`方法来判断指定的 `Optional` 对象是否为空。

```java
var op = Optional.empty();
System.out.println(op.isEmpty());//判断指定的 Optional 对象是否为空
```

## Lambda 参数的局部变量语法

从 Java 10 开始，便引入了局部变量类型推断这一关键特性。类型推断允许使用关键字 var 作为局部变量的类型而不是实际类型，编译器根据分配给变量的值推断出类型。

Java 10 中对 var 关键字存在几个限制

- 只能用于局部变量上
- 声明时必须初始化
- 不能用作方法参数
- 不能在 Lambda 表达式中使用

Java11 开始允许开发者在 Lambda 表达式中使用 var 进行参数声明。

```java
// 下面两者是等价的
Consumer<String> consumer = (var i) -> System.out.println(i);
Consumer<String> consumer = (String i) -> System.out.println(i);

```

