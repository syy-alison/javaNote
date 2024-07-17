[TOC]



# 1. 概述

## 1.1. 什么是消息队列

- 消息队列是一种进程间通信或者同一进程的不同线程间的通信方式。

- 是一个存放消息的容器。消息发布者只管把消息发布到MQ中而不管谁来取，消息使用者只管从MQ中取消息而不管是谁发布的，这样发布者和使用者都不知道对方的存在。
- 主要解决应用耦合，异步消息，流量削峰等问题，实现高性能，高可用，可伸缩和最终一致性架构。是大型分布式系统不可缺少的中间件。

![1714302901693-80f1a3bd-508f-42f6-9d5e-f5b742a70ba4.png](assets/1714302901693-80f1a3bd-508f-42f6-9d5e-f5b742a70ba4.png)

## 1.2. 使用场景

- **异步处理（提高系统性能）**：某些耗时较大但不不影响主线程的操作，可以通过MQ的方式异步进行处理，可以减少系统响应时间。
- **应用解耦**：比如系统A进行某项操作之后，通知系统B和C，系统BC接收到消息后进行相同的处理，假如B系统需要下线或者新增一个系统时，就需要改整个系统的代码，如此反复添加和删除依赖的系统，系统便难以维护，此时可以通过MQ来进行解耦。
- **流量削峰**：先将短时间高并发产生的事务消息存储在消息队列中，然后后端服务再慢慢根据自己的能力去消费这些消息，这样就避免直接把后端服务打垮掉。举例：在电子商务一些秒杀、促销活动中，合理使用消息队列可以有效抵御促销活动刚开始大量订单涌入对系统的冲击。
- **延迟处理：**消息发送后不会立即被消费，而是指定一个时间，到时间后再消费。
- **顺序保证**：在很多应用场景中，处理数据的顺序至关重要。消息队列保证数据按照特定的顺序被处理，适用于那些对数据顺序有严格要求的场景
- **数据流处理**：针对分布式系统产生的海量数据流，如业务日志、监控数据、用户行为等，消息队列可以实时或批量收集这些数据，并将其导入到大数据处理引擎中，实现高效的数据流管理和处理。

## 1.3. 消息队列协议

**为了让消息发送者和消息接收者都能够明白消息所承载的信息**（消息发送者需要知道如何构造消息；消息接收者需要知道如何解析消息）**，它们就需要按照一种统一的格式描述消息，这种统一的格式称之为消息协议**。所以，**有效的消息一定具有某一种格式；而没有格式的消息是没有意义的**。

### 1.3.1. AMQP

AMQP即Advanced Message Queuing Protocol,是应用层协议的一个开放标准，为面向消息的中间件设计，消息中间件主要用于组件之间的解耦，消息的发送者无需知道消息使用者的存在，反之亦然。他是具有现代特征的二进制协议：多通道的，协商的，异步的，安全的，便捷的，自然的，高效的。

**AMQP（0.9.1）通常划分为2层：**

功能层：定义了一系列命令，分成功能独立的逻辑类，可为应用程序做有用工作。

传输层：将这些方法从应用程序应用搬到服务器并返回，它同时会处理通道复用，帧同步，内容编码，心跳检测以及数据表示和错误处理。

**AMQP（0.10）变化较大，分为3层：**

模型层：定义一套命令，按照功能分类，客户端应用可以利用这些命令来实现它的业务功能。

会话层：负责将命令从客户端应用传递给服务器，再将服务器的应答传递给客户端应用，会话层为这个传递过程提供可靠性，同步机制和错误处理。

传输层：提供帧处理，信道复用，错误检测和数据表示。

AMQP 0.10在灵活度增加的同时复杂度也增加了。

**AMQP模型**

表示关键实例和语义的逻辑框架，它必须对兼容AMQP实现的服务器可用，使得服务的状态可以通过客户端按本规范中定义的语义来实现。

![image-20240620140119969](assets/image-20240620140119969.png)

消息被发布者发送给交换机，交换机常常被比喻为邮局或者邮箱，交换机将受到的消息按照路由规则分发到绑定的队列中，最后AMQP代理会将消息投递给订阅了此队列的消费者，或者消费者按需获取。

**协议特点：面向消息，队列，路由（包括点对点和发布/订阅），可靠性，安全。**

### 1.3.2. MQTT

MQTT即Message Queue Telemetry Transport,消息队列遥测传输，是IBM开发的一个即时通讯协议，是一种基于轻量级代理的，发布/订阅模式的消息传输协议，运行在TCP协议栈智商，为其提供有序，可靠，双向连接的网络连接保证。该协议支持所有平台，几乎可以把所有联网物品和外部连接其他，被用来当做传感器和致动器的通信协议。

![1714304708207-71d2d11d-db99-4911-bd9e-b9813cb76cba.png](assets/1714304708207-71d2d11d-db99-4911-bd9e-b9813cb76cba.png)

**协议特点**：格式简单，占用带宽小，移动端通信，PUSH，嵌入式系统

### 1.3.3. STOMP

STOMP（Streaming Text Orientated Message Protocol）是流文本定向消息协议，是一种MOM（Message Orientated Middieware，面向消息的中间件）设计的简单文本协议，STOMP提供了一个可互操作的连接格式，允许客户端与任意STOMP消息代理（Broker）进行交互。

协议特点：命令模式（非topic\queue模式）

### 1.3.4. XMPP

XMPP（可扩展消息处理现场协议，Extensible Messaging and Presence Protocol）是基于可扩展标记语言（XML）的协议，多用于即时消息以及在线现场探测，适用于服务器之间的准即时操作，核心是基于XML流传输，这个协议可能最终允许因特网用户向因特网上的其他任何人发送即时消息，即使其操作系统和浏览器不同。

协议特点：通用公开，兼容性强，可扩展，安全性高，但是XML编码格式占用带宽大。

## 1.4. 常见消息队列

### 1.4.1. RabbitMQ

RabbitMQ是实现AMQP（0.9.1）协议的消息中间件的一种，由RabbitMQ Technologies Ltd 开发并且提供商业支持的，最终起源于金融系统，服务器端用Erlang语言编写，用于在分布式系统中存储转发消息，在易用性，扩展性，高可用性等方面表现较好。

![img](assets/1714308886541-e929c1fc-0ceb-4dbd-81a3-142a0fd511b4.png)

**组成元素**

- 元素包括：Producer(生产者)，Consumer(消费者)，Broker(代理服务器)，Virtual Host(虚拟节点)，Exchange(交换机)，Message(消息)，Queue(队列)
- 一个Broker中一定包含完整的Virtual Host，Exchange，Queue定义，一个Broker可以创建多个Virtual Host,如果是有多个Broker构成的集群提供服务，那么一个Virtual Host也可以有多个Broker共同构成。
- Producer生产消息，将消息发送给Broker，Consumer消费消息，负责从broker中获取消息，
- Connection是由Producer和Consumer创建的连接，连接到Broker物理节点上，但是有了Connection之后客户端还不能和服务端通信，在Connection之上客户端会创建Channel，连接到Virtual Host或者Queue上，这样客户端才能向Exchange发送消息或者从Queue接收消息，一个Connection上允许存在多个Channel，只有Channel中才能够发送/接收消息。
- Exchange可以绑定多个Queue也可以同时绑定其他Exchange,消息通过Exchange时，会按照Exchange中设置的Routing规则，将消息发送到符合的Queue或者Exchange中。

**消息路由**

1. Producer会先建立Channel，建立到Broker上Virtual Host的连接，接下来就可以向这个Virtual Host中的Exchange发消息。
2. Producer把消息发布到Exchange上，消息最终到达队列并被消费者接收，而Binding决定交换机的消息应该发送到哪个队列，Exchange能够处理消息的前提是，它至少已经和某个Queue或者另外的Exchange形成了绑定关系，并设置好了到这些Queue和Exchange的路由规则，在Exchange接受到消息后，会根据设置的路由规则，将消息发送到符合要求的Queue或者Exchange中（路由规则与message中的Routing key属性配合使用）。
3. 当Queue收到消息之后，会进行以下处理：

1. 如果当前没有Consumer的Channel连接到这个Queue，那么Queue将会把这条消息进行存储，直到有Channel被创建。
2. 如果已经有Channel连接到这个Queue，那么消息将会按照顺序发送给这个Channel；

1. 当Consumer收到消息之后，就可以进行消息的处理：

1. Consumer在完成某一条消息的处理后，将需要手动的发送一条ACK消息到对应Queue，也可以设置为自动发送或者无需发送。
2. Queue在接受到这条ACK消息后，才认为这条消息处理成功，并将这条消息从Queue中移除。
3. 如果对应的Channel断开后，Queue都没有这条消息的ACK信息，这条消息将会重新发送给另外的Channel，也可以直接发送NACK信息，这样这条消息将会立即归队，并发送给另外的Channel。

**Exchange类型**

Exchange分发消息时，根据类型的不同，分发策略有明显的区别: Direct,Fanout,Topic,Headers。Headers匹配AMQP消息的Header而不是路由键，此外Headers交换机和Direct交换机完全一致，但是性能差很多，目前几乎不用**。**

- DIRECT
- ![1714310605958-0a9c85d1-d406-4c43-83e5-06a4c0604a17.png](assets/1714310605958-0a9c85d1-d406-4c43-83e5-06a4c0604a17.png)

消息中的路由键如果和Binding中Binding key一致，交换机就将消息发送到对应的队列中，路由键与队列名完全匹配，如果一个队列绑定到交换机要求路由键位news，则只转发Routing key为news的消息，不会转发weather，它是完全匹配，单播的模式。

- FANOUT

![1714310663147-e072cb89-88b0-4bdd-b6a4-672bb901805c.png](assets/1714310663147-e072cb89-88b0-4bdd-b6a4-672bb901805c.png)

每个发到Fanout类型交换器的消息都会分到所有绑定的队列上去，Fanout交换器不处理路由键，只是简单的将队列绑定到交换机上，每个发送到交换器的消息都会被转发到与该交换器绑定的所有队列上，很想子网光比，每台子网内的主机都获得了一份消息的复制。Fanout类型转发消息是最快的。

- TOPIC

![1714311114774-dc6d64b2-8d27-4b62-920f-491e524c053f.png](assets/1714311114774-dc6d64b2-8d27-4b62-920f-491e524c053f.png)

交换机通过模式匹配分配消息的路由键属性，将路由键与某个模式进行匹配，此时队列需要绑定到一个模式上，它将路由键个绑定键的字符串切分为单次，这些单次之间用点隔开。

支持通配符：

- *匹配一个单词
- \#匹配0个或者多个单词

**主要特性**

- **可靠性：**提供了多种技术可以让你在性能和可靠性之间进行权衡，如持久性机制，投递确认，发布确认和高可用机制
- **灵活的路由：**消息在到达队列之前，通过Exchange进行路由，对于典型的路由RabbitMQ提供了一些内置的Exchange，而对于更复杂的路由，则可以将这些Exchange组合起来使用，甚至可以实现自己的Exchange，并且当做RabbitMQ的插件来用。
- **消息集群：**在相同局域网中的多个RabbitMQ服务器聚合在一起，形成一个逻辑Broker.
- **高可用：**队列可以在集群中的机器上进行镜像，以确保在硬件问题下还保证消息安全
- **多协议：**支持多种消息队列协议，如STOMP，MQTT等
- **多语言：**使用Erlang语言编写，客户端几乎支持多种常用语言
- **管理界面：**RabbitMQ有一个易用的web用户界面，使得用户可以方便进行监控和消息的管理
- **跟踪机制：**RabbitMQ提供消息跟踪机制
- **插件机制**：提供了许多的插件来进行扩展，也支持自定义插件的开发。

### 1.4.2. RocketMQ

RocketMQ是阿里巴巴在2012年开源的分布式消息中间件，目前已经捐赠给Apache软件基金会，并于2017年9月25日称为Apache的顶级项目，以其高性能，低延时和高可靠等特性近年来已经也被越来越多的国内企业使用。

![1714312463881-b1356c0e-4fbf-4d11-8caa-e906dc491947.png](assets/1714312463881-b1356c0e-4fbf-4d11-8caa-e906dc491947.png)



**生产者组（Producer）**

负责生产消息，生产者向消息服务器发送由业务应用程序系统生成的消息。RocketMQ提供了三种方式发送消息：同步，异步，单向

**消费者组（Consumer）**

负责消费消息，消费者从消息服务器拉取信息并将其输入用户应用程序，站在用户应用的角度消费者有两种类型：拉取型消费者，推送型消费者。**拉取型消费者**主动从消息服务器拉取信息，只要批量拉取到消息，用户应用就会启动消费过程，所以Pull称为主动消费型，**推送型消费者**封装了消息的拉取，消费进度和其他的内部维护工作，将消息到达执行的回调接口留给用户应用程序来实现，所以push称为被动消费类型，但从实现上看还是从消息服务器中拉取消息，不同于Pull的是Push首先要注册消费监听器，当监听器处触发后才开始消费消息。

**名称服务器（NameServer）**

用来保存Broker相关元信息并给Producer和Consumer查找Broker信息，NameServer被设计称几乎无状态的，可以横向扩展，节点之间相互之间无通信，通过部署多台机器来标记自己是一个伪集群。每个Broker在启动的时候会到NameServer注册，Producer在发送消息前会根据topic到nameServer获取到Broker的路由信息，Consumer也会定时获取Topic的路由信息，所有从功能上看应该是和Zookeeper差不多，据说RocketMQ的早期版本确实使用的是Zookeeper,后来改为了自己实现的NameServer。

**消息服务器（Broker）**

是消息存储中心，主要作用是接受来自于Producer的消息并存储，Consumer从这里取得消息，它还存储与消息相关的元数据，包括用户组，消费进度偏移量，队列信息等。从部署结构图中可以看出Broker有master和slave两种类型。master既可以读，也可以写，slave不可以写只可以读。从物理结构上看Broker的集群部署方式有四种：单master,多maser,多master多slave(同步刷盘)，多master多slave(异步刷盘)

**主要特性**

- **灵活可扩展性**：天然支持集群，其核心四组件（Name Server,Broker,Producer,Consumer）每一个都可以在没有单点故障的情况下进行水平扩展。
- **海量消息堆积**：采用零拷贝原理实现超大的消息的堆积能力，据说单机已可以支持亿级消息堆积，而且在对接了这么多消息后仍然可以保持写入低延迟。
- **顺序消息**：可以保证消息消费者按照消息发送的顺序对消息进行消费，顺序消费分为全局有序和局部有序，一般推荐使用局部有序，即生产者通过将某一类消息按照顺序发送至同一个队列来实现。
- **消息过滤**：分为在服务器端过滤和在消费端过滤，服务端过滤时可以按照消息消费者的要求做过滤，优点是减少不必要的消息传输，缺点是增加了消费服务器的负担，实现相对复杂。消费端过滤则完全由具体应用自定义实现，这种方式更灵活，缺点是很多无用消息会传输给消息消费者。
- **事务消息**：除了支持普通消息，顺序消息之外还支持事务消息，这个特性对于分布式事务来说提供了又一种解决思路。
- **消息回溯**：是指消费者已经消费成功的消息，由于业务上的需求需要重新消息，RocketMQ支持按照时间回溯消费，时间维度精确到毫秒，可以向前回溯，也可以向后回溯。

### 1.4.3. Kafka

Kafka是由Apache软件基金会开发的一个开源流处理平台，由Scala和java编写，kafka是一种高吞吐量的分布式发布订阅消息系统，它可以处理消费者规模的网站中的所有动作流数据。这种动作时在现代网络上的许多社会功能的一个关键因素，这些数据通常是由于吞吐量的要求而通过处理日志和日志聚合来解决。对于像Hadoop一样的日志数据和离线分析系统，但又要求实时处理的限制，这是一个可行的解决方案。kafka的目的是通过Hadoop的并行加载机制来统一处理线上和离线的消息处理，也是为了通过集群来提供实时的消息。



![1714314863315-7d82c20d-e5dc-4c2a-a43b-a01ec4716e1e.png](assets/1714314863315-7d82c20d-e5dc-4c2a-a43b-a01ec4716e1e.png)



**基本组件**

- Broker：消息中间件处理节点，一个Kafka节点就是一个Broker，一个或者多个Broker可以组成一个Kafka集群
- Topic：每条发布到kafka集群的消息都有一个类别，这个类别被称为Topic。（物理上不同topic的消息分开存储，逻辑上一个Topic的消息虽然保存于一个或者多个Broker上但用户只需指定消息的Topic即可生产或者消费数据而不必关心数据存在何处）
- Partition：用于存放消息的队列，存放的消息都是有序的，同一个主题可以分为多个partation，如分为多个partation,同样会以如partation1存放1，3，5消息，partation2存放2，4，6消息
- Producer：消息生产者，向Broker发送消息的客户端
- Consumer：消息消费者，从Broker读取消息的客户端，Consumer是通过offset进行标识消息被消费的位置。
- Consumer Group : 每个Consumer属于一个特定的Consumer Group，一条消息可以发送到多个不同的Consumer Group,但是同一个consumer Group中只能有一个consumer能够消费该消息。

主要特性：

1**.快速持久化**：可以在 O(1) 的系统开销下进行消息持久化 

**2.高吞吐**：在一台普通的服务器上既可以达到10W/s的吞吐速率

3.**完全的分布式系统**：Broker、Producer和Consumer都原生自动支持分布式，自动实现负载均衡 

4.**零拷贝技术(zero-copy)**：减少IO操作步骤，提高系统吞吐量 

5.支持同步和异步复制两种高可用机制 

6.丰富的消息拉取模型，支持数据批量发送和拉取 

7.数据迁移、扩容对用户透明 

8.无需停机即可扩展机器 

9.高效订阅者水平扩展、实时的消息订阅、亿级的消息堆积能力、定期删除机制

### 1.4.4. ActiveMQ

ActiveMQ 是由 Apache 出品的一款开源消息[中间件](https://cloud.tencent.com/product/tdmq?from_column=20065&from=20065)，旨在为应用程序提供高效、可扩展、稳定、安全的企业级消息通信。它的设计目标是提供标准的、面向消息的、多语言的应用集成消息通信中间件。ActiveMQ 实现了 JMS 1.1 并提供了很多附加的特性，比如 JMX 管理、主从管理、消息组通信、消息优先级、延迟接收消息、虚拟接收者、消息持久化、[消息队列](https://cloud.tencent.com/product/cmq?from_column=20065&from=20065)监控等等。它非常快速，支持多种语言的客户端和协议，而且可以非常容易的嵌入到企业的应用环境中，并有许多高级功能。

![image-20240620140623485](assets/image-20240620140623485.png)

**基本组件**

Broker,Producer,Consumer,Topic,Queue,Message

**连接器**

ActiveMQ Broker的主要作用是为客户端应用提供一种通信机制，为此ActiveMQ提供看一种连接机制，并用连接器（connector）来描述这种连接机制，ActiveMQ中连接器有两种，一种是用于客户端与消息代理服务器（client-to-broker）之间通信的传输连接器（transport connector），一种是用于消息代理服务器之间（broker-to-broker）通信的网络连接器（network connector）。

**消息传送模型**

1. 点对点模型（Point to Point）

   ![1714355530654-e8f8e8a0-d3cf-4e68-9506-3ab537ccc0f0.png](assets/1714355530654-e8f8e8a0-d3cf-4e68-9506-3ab537ccc0f0.png)

使用队列（Queue）作为消息通信载体，满足生产者和消费者模式，一条消息只能被一个消费者使用，未被消费的消息在队列中保留直到被消费或者超时。

1. 发布订阅模型（Pub/Sub）

![1714355464902-05826165-3676-49e4-a8a3-09a3bcd912e0.png](assets/1714355464902-05826165-3676-49e4-a8a3-09a3bcd912e0.png)

消息域使用topic作为Destination,发布者向topic发送消息，订阅者注册接受来自topic的消息，发送到topic的任何消息都将自动传递给所有订阅者。

**主要特性**

- 服从JMS规范：完全支持JMS 1.1和J2EE 1.4规范，包括同步或者异步的消息分发，一次和仅一次的消息分发，分布式事务消息，消息接受，订阅，持久化等。
- 连接灵活性：ActiveMQ提供了多种连接模式，例如in-VM，TCP，SSL，NIO，UDP，多播，JGroup.JXTA等
- 多协议：openWire,SMTOP,REST,XMPP,AMQP等
- 多语言：支持java，C/C++，python,PHP ,Perl,.net等
- 代理集群：多个ActiveMQ代理可以组成一个集群来提供服务
- 简单的管理：ActiveMQ 是以开发者思维被设计的，所以它并不需要专门的管理员，因为它提供了简单又实用的管理特性，有很多方法可以监控ActiveMQ不同层面的数据，包括使用在Jconsole或者在ActiveMQ的Web Console中使用JMX。通过处理JMX的告警信息，通过使用命令行脚本，甚至可以通过监控各种类型的日志。
- 整合容易：ActiveMQ可以通过Spring的配置文件方式很容易嵌入到Spring应用中，也可以轻松的与CXF，Axis等Web Service技术整合，以提供可靠的消息传输。

### 1.4.5. 对比

- ActiveMQ 的社区算是比较成熟，但是较目前来说，ActiveMQ 的性能比较差，而且版本迭代很慢，不推荐使用，已经被淘汰了。
- RabbitMQ 在吞吐量方面虽然稍逊于 Kafka、RocketMQ 和 Pulsar，但是由于它基于 Erlang 开发，所以并发能力很强，性能极其好，延时很低，达到微秒级。但是也因为 RabbitMQ 基于 Erlang 开发，所以国内很少有公司有实力做 Erlang 源码级别的研究和定制。如果业务场景对并发量要求不是太高（十万级、百万级），那这几种消息队列中，RabbitMQ 或许是你的首选。
- RocketMQ 和 Pulsar 支持强一致性，对消息一致性要求比较高的场景可以使用。
- RocketMQ 阿里出品，Java 系开源项目，源代码我们可以直接阅读，然后可以定制自己公司的 MQ，并且 RocketMQ 有阿里巴巴的实际业务场景的实战考验，支持的功能比较多（比如定时消息）。
- Kafka 的特点其实很明显，**就是仅仅提供较少的核心功能**，运维比较困难（配置比较多），对带宽有一定要求（多副本）。但是提供超高的吞吐量，ms 级的延迟，极高的可用性以及可靠性，而且分布式可以任意扩展。同时 Kafka 最好是支撑较少的 topic 数量即可，保证其超高吞吐量。Kafka 唯一的一点劣势是有可能消息重复消费，那么对数据准确性会造成极其轻微的影响，在大数据领域中以及日志采集中，这点轻微影响可以忽略这个特性天然适合大数据实时计算以及日志收集。如果是大数据领域的实时计算、日志采集等场景，用 Kafka 是业内标准的，绝对没问题，社区活跃度很高，绝对不会黄，何况几乎是全世界这个领域的事实性规范。



| 特性                    | RabbitMQ                                                     | RocketMQ                                                     | Kafka                                                        | ActiveMQ                             |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------ |
| 开发语言                | Erlang                                                       | java                                                         | Scala&java                                                   | java                                 |
| 客户端支持              | 官方支持Erlang，java,Ruby等，社区产出多语言API，几乎支持所有常用语言 | java,c++                                                     | 官方支持java,社区有多语言版本，如PHP，Go，C/C++.Ruby,NodeJs等 | java，C/C++，python,PHP ,Perl,.net等 |
| 协议支持                | AMQP,XMPP,SMTP,SMTOP                                         | 自定义协议，社区提供JMS                                      | 自定义协议，社区提供了HTTP协议支持                           | openWire,SMTOP,REST,XMPP,AMQP        |
| 可用性                  | 高，基于主从架构实现高可用                                   | 很高，分布式架构                                             | 很高，分布式，一个数据多个副本，少数机器宕机，不会丢失数据，不会导致不可用 | 高，基于主从架构实现高可用           |
| 集群                    | 支持                                                         | 支持                                                         | 支持                                                         | 支持                                 |
| 负载均衡                | 支持                                                         | 支持                                                         | 支持                                                         | 支持                                 |
| 单机吞吐量              | 万级                                                         | 十万级                                                       | 十万级                                                       | 万级                                 |
| topic数量对吞吐量的影响 | -                                                            | topic达到几百/几万的级别后，吞吐量会有较小幅度的下降，在同等机器下，可以支持大量topic | topic从几十到几百的时候，吞吐量会大幅度下降，因为kafka的每个topic，每个分区都会对应一个物理文件，若需要支撑大规模的topic，则需要增加更多的机器资源 | -                                    |
| 消息批量操作            | 不支持                                                       | 支持                                                         | 支持                                                         | 支持                                 |
| 消息推拉模式            | pull/push均支持                                              | pull/push均支持                                              | pull                                                         | pull/push均支持                      |
| 消息可靠性              | 可以做到不丢失                                               | 可以做到不丢失                                               | 可以做到不丢失                                               | 有较低的概率丢失数据                 |
| 消息延迟                | 微妙级（最快）                                               | 毫秒级                                                       | 毫秒级                                                       | 毫秒级                               |
| 持久化能力              | 内存，文件，支持数据堆积，但是影响生产速率                   | 磁盘文件                                                     | 磁盘文件，只要容量够，可以做到无限堆积                       | 内存，文件，数据库                   |
| 事务消息                | 不支持                                                       | 支持                                                         | 不支持                                                       | 支持                                 |
| 管理界面                | web管理界面                                                  | web管理界面                                                  | web管理界面                                                  | web管理界面                          |

## 1.5. 消息队列的问题

- **系统可用性降低：** 系统可用性在某种程度上降低，为什么这样说呢？在加入 MQ 之前，你不用考虑消息丢失或者说 MQ 挂掉等等的情况，但是，引入 MQ 之后你就需要去考虑了！
- **系统复杂性提高：** 加入 MQ 之后，你需要保证消息没有被重复消费、处理消息丢失的情况、保证消息传递的顺序性等等问题！
- **一致性问题：** 我上面讲了消息队列可以实现异步，消息队列带来的异步确实可以提高系统响应速度。但是，万一消息的真正消费者并没有正确消费消息怎么办？这样就会导致数据不一致的情况了。

# 2. Kafka

https://geekdaxue.co/read/haofeiyu@kafka/ok8sod

## 2.1. 概述

Apache Kafka项目旨在提供统一的，高吞吐量，低延迟的平台来处理实时数据流，Kafka可以通过Kafka Connect连接到外部系统，并提供了Kafka Streams（一种Java流处理库），Kafka使用经过优化的二进制TCP协议，并使用抽象"message set"将消息分组以减少网络开销并且可以支撑更大的网络数据包，从而使Kafka可以将突发的随机消息写入流转化为线性写入。

| 特性              | 分布式             | 高性能           | 持久性和扩展性 |
| ----------------- | ------------------ | ---------------- | -------------- |
| 描述              | 多分区             | 高吞吐量         | 数据可持久化   |
| 多副本            | 低延迟             | 容错性           |                |
| 多订阅者          | 高并发             | 支持水平在线扩展 |                |
| 基于Zookeeper调度 | 时间复杂度为O（1） | 消息自动平衡     |                |

## 2.2. 架构设计

### 2.2.1. 设计思想

一个最基本的架构是生产者发布一个消息到Kafka的一个Topic，该Topic的消息存放于Broker中，消费者订阅这个Topic，然后从Broker中消费消息。

![1714356969568-5c289b1b-ec93-4d0f-a583-a8d1a11c2212.png](assets/1714356969568-5c289b1b-ec93-4d0f-a583-a8d1a11c2212.png)

上面所示的架构分为三部分：Producer,Kafka Broker,Consumer Group,它们分别运行在不同的节点，下面概括介绍一下Kafka的设计思想

- **Consumer Group** ：Kafka是按照消费组来消费信息，一个消费组下面的所有机器可以组成一个Consumer Group,每条消息只能被该Consumer Group中的一个Consumer消费，不同Consumer Group可以消费同一条消息。
- **消息状态**：在Kafka中，消息是否能被消费的状态保存在Consumer中，Broker不会关心消息是否被消费或者被谁消费，Consumer会记录一个offset值（指向partition中下一条将要被消费的消息位置），如果offset被错误设置可能导致同一条消息被多次消费或者消息丢失。
- **消息持久化**：Kafka会把消息持久化到本地文件系统中，并且具有极高的性能。
- **批量发送**：Kafka支持以消息集合为单位进行批量发送，以提高效率。
- **Push-and-Pull**：Kafka中的Producer和Consumer采用的是Push-and-Pull模式，即Producer向Broker Push消息，Consumer从Broker Pull消息。
- **分区机制（partition）**：Kafka的Broker端支持消息分区，Producer可以决定把消息发到哪个partition，在一个partition中消息的顺序就是Producer发送消息的顺序，一个Topic中的partition是可配置的，partition是Kafka高吞吐量的重要保证。

### 2.2.2. 系统架构



![1714357744446-beeeda62-bbab-482b-83ed-d92f162993a0.png](assets/1714357744446-beeeda62-bbab-482b-83ed-d92f162993a0.png)



如上图所示，一个典型的kafka集群包含若干个Producer，Broker, Consumer Group以及一个zookeeper集群，Kafka通过zookeeper集群管理Broker集群，Producer使用Push模式将消息发送到Broker，Consumer Group使用pull模式从Broker订阅并消费消息。

- **Broker：**一个Kafka集群中的一台服务器就是一个Broker，Broker可以水平无限扩展，同一个Topic中的消息可以分布在多个Broker中
- **Consumer :** consumer通过向Broker发送一个“Fetch”请求来回去他想要消费的消息，Consumer的每个请求都在消息文件中指定了对应的offset，并接收从该位置开始的一大块数据，因此，Consumer对于该位置的控制就显得极为重要，并且可以在需要的时候通过回退到某个位置再次消费对应的数据。
- **Producer：**将客户端生产的message发送到Broker中的Partition Leader节点，Partition可以通过配置保证写入的消息不会丢失，Producer同时支持消息异步发送，批量发送。
- **Push vs Pull** : 作为一个消息系统，kafka遵循了传统的方式，选择由Producer向Broker Push 消息，一些logging-centric system，比如Facebook的Scribe和Cloudera 的Flume,采用Push模式，事实上，push模式和pull模式各有优劣，Push模式很难适应消费速率不同的消费者，因为消息发送速率是由Broker决定的，Push模式的目的是尽可能以最快速度传递消息，但是这样很容易造成Consumer来不及处理消息，典型的表现就是拒绝服务以及网络拥塞。而pull模式可以根据Consumer的消费能力以适当的速率消费消息，对于Kafka而言，Pull模式更合适。Pull模式可以简化Broker的设计，Consumer可以自主控制消费消息的速率，同时Consumer可以自己控制消费方式（即可批量消费也可逐条消费），同时还能选择不同的提交方式从而实现不同的传输语义。
- **Topic & Partition：**Topic在逻辑上可以被认为是一个Queue，Kafka的每条消息都必须指定一个Topic，一个Topic中的消息可以分布在集群中的多个Broker中 ，Consumer根据订阅的Topic到对应的Broker上去拉取消息。为了提升整个集群的吞吐量，物理上一个Topic可以分成多个Partition，每个Partition在磁盘上对应一个文件夹，该文件夹存放了这个Partition的所有消息文件和索引文件，假设topic1和topic2两个topic,且分别有13和19个分区，则整个集群会生成32个文件夹。每个消息文件都是一个log entry序列。

![image-20240620142949837](assets/image-20240620142949837.png)

**一条完整的消息包含RECORD、offset以及message size。**其中offset用来标识它在Partition中的偏移量，这个offset是逻辑值，而非实际物理偏移值，message size表示消息的大小。与消息对应的还有消息集的概念，消息集中包含一条或者多条消息，消息集不仅是存储于磁盘以及在网络上传输（Produce & Fetch）的基本形式，而且是kafka中压缩的基本单元，详细结构参考上图右侧。下面来具体描述一下消息（RECORD）格式中的各个字段，从crc32开始算起，各个字段的解释如下：

- crc32（4B）：crc32校验值，校验范围为magic至value之间。
- magic（1B）：消息格式版本号，0.9.X版本的magic值为0。
- attributes（1B）：消息的属性，总共占1个字节，低3位表示压缩类型：0表示NONE、1表示GZIP、2表示SNAPPY、3表示LZ4，其余位保留。
- key length（4B）：表示消息的key的长度。如果为-1，则表示没有设置key，即key=null。
- key：可选，如果没有key则无此字段。
- value length（4B）：实际消息体的长度。如果为-1，则表示消息为空。
- value：消息体，可以为空。 

消息发送到Broker后，每条消息都被顺序写该Partition所对应的文件中，因此效率非常高，这是Kafka高吞吐率的一个很重要的保证。

![image-20240620143036925](assets/image-20240620143036925.png)

这里要注意，因为Kafka读取消息的时间复杂度为O(1)，即与文件大小无关，所以这里删除过期文件与提高Kafka性能无关。另外，Kafka会为每一个Consumer Group保留一些metadata信息（当前消费的消息的位置，即offset）。这个offset由Consumer控制，Consumer会在消费完一条消息后递增该offset。当然，Consumer也可将offset设成一个较小的值，重新消费一些消息。因为offet由Consumer控制，所以Kafka Broker是无状态的，它不需要标记消息是否被消费过，也不需要通过Broker去保证同一个Consumer Group只有一个Consumer能消费某一条消息，因此也就不需要锁机制，从而保证了Kafka的高吞吐率。 下图中，Consumer 1、2分属于不同的Consumer Group，Consumer 2的offset =4，Consumer 1的offset=3，这表明Consumer Group 1中的Consumer下次会从offset = 3 的message读取， Consumer Group 2中的Consumer下次会从offset = 4 的message读取。注意 这里并没有说是Consumer 1 下次会从offset = 3 的message读取，原因是Consumer 1可能会退出Group ，然后Consumer Group 1 进行重新分配分区。

![1714360305291-d88b9994-d8a6-433b-b02f-49e4e1f424f2.png](assets/1714360305291-d88b9994-d8a6-433b-b02f-49e4e1f424f2.png)

### 2.2.3. 消息发送

- **Producer发送消息到对应broker时，会根据Paritition机制选择将消息存储到哪一个Paritition，机制主要有轮询策略，随机策略，和按照key保序的策略，也可以自定义策略。**

Producer其主要功能是负责向Broker发送消息，工作原理如下图所示：

![1714360722169-56520ee9-0858-4191-80c0-672dd0591ace.png](assets/1714360722169-56520ee9-0858-4191-80c0-672dd0591ace.png)

**Producer发送消息到对应broker时，会根据Paritition机制选择将消息存储到哪一个Paritition**，如果Paritition机制设计合理，所有消息可以均匀分布到不同的Paritition里，这样就实现了负载均衡，如果一个Topic对应一个文件，那这个文件所在的机器I/O将成为这个topic的性能瓶颈，而有了Paritition之后，不同的消息可以并行写入不同的Paritition中，极大的提高了吞吐率，**所谓的Paritition机制也就是Producer消息partitioning策略，具体有以下几种策略。**

- **轮询策略**

  - 轮询策略是kafka java客户端生产者的默认策略
  - 轮询策略的负载均衡表现的非常优秀，总能保证消息最大限度的被平均分配到所有分区，默认情况下他是最合理的分区策略，如下图所示：

  ![image-20240620142637231](assets/image-20240620142637231.png)

- **随机策略**
  - **随机策略默认从Partition列表中随机选择一个**，随机策略的消息分布大致如下图所示。


![image-20240620142715035](assets/image-20240620142715035.png)

- **按消息键保序策略**
  - kafka允许为每条消息定义消息键，简称key
  - key可以是一个有明确业务含义的字符串
  - **一旦消息被定义了key,可以保证同一Key的所有消息都放入到相同的分区里，由于每个分区下的消息处理都是顺序的，所以这个策略被称为按照消息键保序策略。**

- **自定义策略**
  - 自定义的分区策略，需要显示的配置生产者的参数partitioner.class
  - 实现接口：org.apache.kafka,clients.producer.partitioner


### 2.2.4. 消息消费(Rebalance)

- 每个Consumer group保存自己的位移信息，表示要消费的下一条消息的offset。每个消费者根据策略来消费Partition的消息，策略主要有两种，一种是轮询策略，另一种是根据消费者的消费能力进行计算，算出每个消费者消费的分区数量。

- 老版本的位移是提交到zookeeper中的，但是zookeeper其实并不是和进行大批量的读写操作，尤其是写操作。从0.9版本开始kafka提供了另一种解决方案：Broker 端增加了_consumer_offsets这个topic，将offset信息写入这个topic，这样consumer就不需要依赖zookeeper。`enable.auto.commit`  控制是自动提交还是手动提交

  - 自动提交：**Kafka 会保证在开始调用 poll 方法时，提交上次 poll 返回的所有消息。从顺序上来说，poll 方法的逻辑是：先提交上一批消息的位移，再处理下一批消息，因此它能保证不出现消费丢失的情况。但自动提交位移的一个问题在于，它可能会出现重复消费。**
  - 手动提交：它的好处就在于更加灵活，你完全能够把控位移提交的时机和频率。它也有一个缺陷，就是在调用 commitSync() 时，Consumer 程序会处于阻塞状态，直到远端的 Broker 返回提交结果，这个阻塞状态才会结束。
    - 同步提交
    - 异步提交

- **Rebalance（重平衡）**

  - 触发条件

    - **消费组组成员数发生变更。**比如有新的 Consumer 实例加入组或者离开组，抑或是有 Consumer 实例崩溃被“踢出”组。
    - **订阅主题数发生变更（消费组订阅了新的主题）**。Consumer Group 可以使用正则表达式的方式订阅主题，比如 consumer.subscribe(Pattern.compile(“t.*c”)) 就表明该 Group 订阅所有以字母 t 开头、字母 c 结尾的主题。在 Consumer Group 的运行过程中，你新创建了一个满足这样条件的主题，那么该 Group 就会发生 Rebalance。
    - **订阅的主题分区数发生变更。**Kafka 当前只能允许增加一个主题的分区数（言外之意就是：不允许减少主题的分区数）。当分区数增加时，就会触发订阅该主题的所有 Group 开启 Rebalance。 

  - 问题

    - Rebalance 影响 Consumer 端 TPS。总之就是，在 Rebalance 期间，Consumer 会停下手头的事情，什么也干不了。
    - Rebalance 很慢。如果你的 Group 下成员很多，就一定会有这样的痛点。还记得我曾经举过的那个国外用户的例子吧？他的 Group 下有几百个 Consumer 实例，Rebalance 一次要几个小时。在那种场景下，Consumer Group 的 Rebalance 已经完全失控了。
    - Rebalance 效率不高。当前 Kafka 的设计机制决定了每次 Rebalance 时，Group 下的所有成员都要参与进来，而且通常不会考虑局部性原理，但局部性原理对提升系统性能是特别重要的。

  - 避免

    - 未能及时发送心跳导致的 Rebalance：需要仔细地设置 session.timeout.ms 和 heartbeat.interval.ms 的值。我在这里给出一些推荐数值，你可以“无脑”地应用在你的生产环境中。设置 session.timeout.ms = 6s。设置 heartbeat.interval.ms = 2s

      要保证 Consumer 实例在被判定为“dead”之前，能够发送至少 3 轮的心跳请求，即 session.timeout.ms >= 3 * heartbeat.interval.ms。

    - Consumer 消费时间过长导致 Rebalance：max.poll.interval.ms 它限定了 Consumer 端应用程序两次调用 poll 方法的最大时间间隔。它的默认值是 5 分钟，表示你的 Consumer 程序如果在 5 分钟之内无法消费完 poll 方法返回的消息，那么 Consumer 会主动发起“离开组”的请求，Coordinator 也会开启新一轮 Rebalance。 


kafka消费者API封装了对集群一系列Broker的访问，可以透明的消费topic中的数据，消费者在消费的过程中需要记录自己消费了多少数据，很多消息引擎都会把这部分信息维护在服务器端，这样做的好处是实现简单，但是有三个问题：1. Broker从此变成有状态的，会影响伸缩性；2 需要引入应答机制增加了系统的复杂度；3 由于要保存很多consumer的offset信息，必然引入复杂的数据结构，造成资源浪费。而kafka的方案是**每个Consumer group保存自己的位移信息，那么只需要简单的一个整数表示位置就够了，同时可以引入Checkpoint机制定期持久化，简化了应答机制的实现。**

**老版本的位移是提交到zookeeper中的，但是zookeeper其实并不是和进行大批量的读写操作，尤其是写操作。从0.9版本开始kafka提供了另一种解决方案：增加了_consumer_offsets这个topic，将offset信息写入这个topic，这样consumer就不需要依赖zookeeper。** 位移主题的key: **<GroupID，主题名，分区号 >**。value保存了位移信息。

![image-20240620142803876](assets/image-20240620142803876.png)

**kafka的consumer group是采用pull的方式来消费消息，那么每个Consumer该消费哪个Partition的消息则需要一套严格的机制来保证，**而且partition是可以水平无限扩展的，随着partition的扩展Consumer消费的partition也会重新分配，这里就涉及到kafka的消息消费分配策略，在kafka内部存在两种默认的分区分配策略：Range和RoundRobin，当以下事件发生时，Kafka将会进行一次分区分配:

- 同一个consumer group内新增消费者
- 消费者离开当前所属的Group,包括Shuts down或者crashes
- 订阅的主题新增partition

**Range策略**

假设我们有个名为T1的主题，其中包含了5个分区，然后我们有两个消费者（C1,C2）来消费这5个分区里面的数据，而且C1的num.streams = 2,C2的num.streams = 1,（num.streams指的是消费者的消费线程个数）。**Range策略是对每个主题而言的，首先对同一个主题里面的分区按照需要进行排序，并对消费者按照顺序进行排序。**在这个例子中，拍完序的分区将会是：0，1，2，3，4；消费者线程拍完序将会是C1-0,C1-1,C2-0,**然后将partitions的个数除以消费者线程的总数来决定每个消费者线程消费几个分区**。**如果除不尽，那么前面几个消费者线程将会多消费一个分区**，5个分区，3个消费者线程，5/3=1。而且除不尽，那么消费者线程C1-0,C1-1将会多消费一个分区，所以最后分区分配的结果看起来就是这样：C1-0消费0,1分区，C1-1消费2，3分区，C2-0消费4分区。

![image-20240620142830915](assets/image-20240620142830915.png)

如果增加partition，从之前的5个分区变成6个分区，那么最终的分配结果为：C1-0消费0,1分区，C1-1消费2，3分区，C2-0消费4，5分区。

![image-20240620142852291](assets/image-20240620142852291.png)

**RoundRobin（轮询）策略**

**使用RoundRobin策略有两个前提条件必须满足：**

- 同一个Consumer Group里面所有消费者的num.streams必须相等：(避免数据倾斜，简化协调)
- 每个消费者订阅的主题必须相同。

假设前面提到的2个消费者的num.streams = 2,RoundRobin策略的工作原理：将所有主题的分区组成TopicAndPartition列表，然后对TopicAndPartition列表按照hashCode进行排序，在我们的例子里面，假如按照hashCode排完序的topic-partitions依次为T1-5,T1-3,T1-0,T1-2,T1-1,T1-4.我们的消费者线程排序为C1-0,C1-1,C2-0,C2-1,最后分区分配的结果为：C1-0将消费T1-5, T1-1，,C1-1将消费T1-3，T1-4分区，C2-0将消费T1-0分区，C2-1将消费T1-2分区。

![image-20240620145243703](assets/image-20240620145243703.png)





### 2.2.5. 消息可靠性

**通过多副本策略和消息应答来保证消息可靠性。**

Kafka的高可靠性的保障来源于其健壮的副本策略即partition的replication机制，kafka将为每个partition提供多个replication，同时将replication分布到整个集群的其他Broker中，具体的replication数量可以根据参数设置，这里的replication会选举一个Leader节点，其他节点为Follower节点，消息全部发送到Leader然后再通过同步算法同步到Follower节点中，当其中有replication不能工作会重新进行选举，即使部分Broker宕机仍然可以保证整个集群的高可用，消息不丢失。

![image-20240620152327370](assets/image-20240620152327370.png)

与此同时，当producer向leader发送数据时，可以通过request.required.acks参数来设置数据可靠性级别：

- 1  这意味着pruducer在replication中的leader已经成功的收到数据并得到确认后发送下一条message，如果leader宕机了，则会丢失数据。
- 0：这意味着pruducer无需等待来自broker的确认而继续发送下一批消息，这种情况下数据传输效率最高，但是数据可靠性时最低的。
- -1： pruducer需要等待replication中的所有Follower都确认收到数据后才算一次发送完成，可靠性最高，但是也不能保证数据不丢失，比如当replication中只有leader时，这样就变成了ack=1的情况。

### 2.2.6. 应用场景

- **异步通信**：消息中间件在异步通信中用的最多，很多业务流程，如果所有步骤都同步进行可能导致核心流程耗时非常长，更重要的是所有步骤都同步进行一旦非核心步骤失败会导致核心流程整体失败，因此在很多业务流程中kafka就充当了异步通信的角色。
- **日志同步**：大规模分布式系统中的机器非常多而且分散在不同的机房，分布式系统带来的一个明显问题就是业务日志的查看，追踪和分析等行为变得十分困难，对于集群规则在百台以上的系统，查询线上日志非常困难，为了应对这种场景统一日志系统应运而生，日志数据都是海量数据，通常为了不给系统带来额外负担一般会采用异步上报，这里kafka以其高吞吐量在日志处理中得到了很好的应用。
- **实时计算：**随着数据量的增加，离线的计算会越来越慢，难以满足用户在某些场景下的实时性要求，因此很多解决方案中引入了实时计算。很多时候，即使是海量数据，也希望即时查看一些数据指标，实时流计算应用而生。实时流计算有两个特点，一个是实时，随时可以看数据，另一个是流。

## 2.3. 高可用

### 2.3.1. 概述

高可用指系统无间断的执行其功能的能力，代表系统的可用性程度，kafka从0.8版本开始提供了高可用机制，可保证一个或者多个Broker宕机之后，其他Broker以及所有的partition都能继续提供服务，且存储的消息不丢失。

对分布式系统来说，当集群规模上升到一定程度之后，一台或者多台机器宕机的可能性大大增加；**kafka采用多机备份和消息应答确认方式解决了数据丢失问题，并通过一套失败恢复机制解决服务不可用问题。**

### 2.3.2. 消息备份机制

#### 2.3.2.1. 消息备份

Kafka允许同一个partition存在多个消息副本（Replica）,每个partition的副本通常由1个leader及0个以上的Follower组成，**生产者将消息直接发往对应Partition的Leader，Follower会周期的向Leader发送同步请求，Kafka的leader机制在保障数据一致性的同时降低了消息备份的复杂度。**

同一个Partition的Replica不应存储在同一个Broker上，因为一旦该Broker宕机，对应的Partition的所有Replica都无法工作，这就达不到高可用的效果，**为了做好负载均衡并提高容错能力，kafka会尽量将所有的partition以及各partition的副本均匀的分配到整个集群。**

#### 2.3.2.2. ISR

ISR(In-sync replicas)指的是一个Partition中与leader保持同步的Replica的列表（实际存储的是副本所在Broker的BrokerId）,˙这里的保持同步不是指与leader数据保持完全一致，只需在replica.lag.max.ms时间内与Leader保持有效连接，官方解释如下：

- 这个参数的含义是 Follower 副本能够落后 Leader 副本的最长时间间隔，当前默认值是 10 秒。这就是说，只要一个 Follower 副本落后 Leader 副本的时间不连续超过 10 秒，那么 Kafka 就认为该 Follower 副本与 Leader 是同步的，即使此时 Follower 副本中保存的消息明显少于 Leader 副本中的消息。
- Follower 副本唯一的工作就是不断地从 Leader 副本拉取消息，然后写入到自己的提交日志中。如果这个同步过程的速度持续慢于 Leader 副本的消息写入速度，那么在 replica.lag.time.max.ms 时间后，此 Follower 副本就会被认为是与 Leader 副本不同步的，因此不能再放入 ISR 中。此时，Kafka 会自动收缩 ISR 集合，将该副本“踢出”ISR。
- 倘若该副本后面慢慢地追上了 Leader 的进度，那么它是能够重新被加回 ISR 集合的。这也表明，ISR 是一个动态调整的集合，而非静态不变的集合。 
- ISR中所有副本都跟上了Leader，通常只有ISR里的成员才可能被选为Leader。当Kafka中unclean.leader.election.enable配置为true（默认为false）且ISR中所有副本均宕机的情况下，才允许ISR外的副本被选为Leader，此时会丢失部分已应答的数据。

Follower周期性的向Leader发送FetchRquest请求，发送时间间隔配置在replica.fetch.wait.max.ms中，默认值是500。

各Partition的Leader负责维护ISR列表并将ISR的变更同步至zookeeper,被移出ISR的Follower会继续向Leader发FetchRequest请求，试图再次跟上Leader重新进入ISR。

#### 2.3.2.3. ACKs

为了讲清楚ISR的作用，下面介绍一下生产者可以选择的消息应答方式，生产者发送消息中包含acks字段，该字段代表Leader应答生产者之前Leader收到的应答数。

- ack = 0 生产者无需等待服务端的任何确认，消息被添加到生产者套接字缓冲区后就视为已发送，因此ack=0不能保证服务端已收到消息，使用场景较少
- ack = 1 : Leader将消息写入本地日志后无需等待Follower的消息确认就做出了应答。如果Leader在应答消息后立即宕机且其他Follower均未完成消息的复制，则该条消息将丢失。![img](assets/1714396377136-15099e0f-463c-494a-a7b3-c3c833110703.png)

上图左侧稳态场景下，Partition1的数据冗余备份在Broker0和Broker2上，Broker0中的副本与Leader副本因网络开销等因素存在1秒钟同步时间差，Broker0中副本落后124条消息，Broker中的副本存在8秒钟同步时间差，Broker2中的副本落后7224条消息，如果途中的Broker1突然宕机且Broker0被选为Partition1中的Leader，则在Leader宕机前写入的124条消息未同步至Broker0中的副本，这次宕机会造成少量消息丢失。

- ack = all : Leader将等待ISR中的所有副本确认后再做出应答，因此只要ISR中任何一个副本还活着，这条应答过的消息就不会丢失。ack = all是可用性最高的选择，但是等待Follower应答引入的额外的响应时间。Leader需要等待ISR中所有副本做出应答。此时响应时间取决于ISR中最慢的那台机器。

#### 2.3.2.4. LEO&HW

每个kafka副本对象都有下面两个重要属性：

- **LEO（log end offset）**:即日志末端偏移，指向了副本日志中下一条消息的位移值（即一条消息的写入位置）
- **HW（hight watermark**）: 即已同步消息标识，因其类似于木桶效用中短板决定水位高度，故取名高水位线。

所有高水位线以下消息都是已备份过的，**消费者仅可消费各分区Leader高水位线以下的消息**，对于任何一个副本对象而言其HW值不会大于LEO值

Leader的HW值由ISR中所有备份的LEO最小值决定**（Follower在发送FetchFRequest时会在PartitionFetchInfo中携带Follower的LEO）**

![1714397504404-5e1709dd-6685-4eb3-b1ce-c6e9786795c1.png](assets/1714397504404-5e1709dd-6685-4eb3-b1ce-c6e9786795c1.png)

Kafka原本使用HW来记录副本的备份进度，HW值的更新通常需要额外一轮FetcheRequest才能完成，存在一些边缘案例导致备份数据丢失或导致多个备份间的数据不一致。Kafka新引入了Leader epoch解决了HW 截断产生的问题。

### 2.3.3. 故障恢复

Kafka从0.8版本开始引入了一套Leader选举及失败恢复机制，首先需要在集群中所有Broker中选出一个Controller，负责向各Partition的Leader选举以及Replica的重新分配，当出现Leader故障后，Controller会将Leader/Fllower的变动通知到为此做出响应的Broker.

Kafka使用Zookeeper存储Broker，topic等状态数据，Kafka集群中的Controller和Broker会在Zookeeper指定节点上注册Watcher（时间监听器），以便在特定事件触发时，由zookeeper将事件通知到对应的Broker。

#### 2.3.3.1. Broker故障恢复

**场景1：Broker与其他Broker断开连接**

由于只是Broker与其他Broker断开连接，Zookeeper还能接收到Broker0的心跳，因此Zookeeper认为Broker依然存活。则对于：

![image-20240620151747986](assets/image-20240620151747986.png)

- **partition0**

Broker0中的副本为partition0的Leader，当Broker0超过replica.lag,time.max.ms没接收到Broker1，Broker2的FetchRequest请求后，Broker0选择将P0的ISR收缩到仅剩Broker0本身，并将ISR的变更同步到zookeeper，Broker0需要根据min.insync.replicas（用于控制副本同步的最小数量）的配置决定是否继续接收生产者数据。

- **partition1**

超过replica.lag.time.max.ms后，Broker会将Broker0中的副本从Partition1的ISR中移除，若后续Broker0恢复连接并赶上了Broker1，则Broker1还会再将Broker0重新加入Partition1的ISR。

**场景2：Broker与zookeeper断开连接**

Broker0与ZooKeeper断开连接后，ZooKeeper会自动删除该Broker对应节点，并且认为Broker0已经宕机。

- **Partition0**       

ZooKeeper删除节点后，该节点上注册的Watcher会通知Controller，Controller会发现Broker0为Partition0的Leader，于是从当前存活的ISR中选择了Broker2作为Partition0的新Leader。Controller通过LeaderAndIsrRequest将Leader变更通知到Broker1、Broker2，于是Broker1改向Broker2发送Partition0数据的FetchRequest请求。

​     生产者每隔60秒会从bootstrap.servers中的Broker获取最新的metadata，当发现Partition0的Leader发生变更后，会改向新Leader-Broker2发送Partition0数据。另一边，Broker0收不到ZooKeeper通知，依然认为自己是Partition0的Leader；由于Broker1、Broker2不再向Broker0发送FetchRequest请求，缺失了ISR应答的Broker0停止写入acks=all的消息，但可以继续写入acks=1的消息。在replica.lag.time.max.ms时间后，Broker0尝试向ZooKeeper发送ISR变更请求但失败了，于是不再接收生产者的消息。

​      当Broker0与ZooKeeper恢复连接后，发现自己不再是Partition0的Leader，于是将本地日志截断(为了保证和Leader数据一致性)，并开始向Broker2发送FetchRequest请求。**在Broker0与ZooKeeper失联期间写入Broker0的所有消息由于未在新Leader中备份，这些消息都丢失了。**

- **Partition1**     

Broker0中的副本只是作为Partition1的Follower节点，而Broker0与Broker1依然保持连接，因此Broker0依然会向Broker1发送FetchRequest。只要Broker0能继续保持同步，Broker1也不会向ZooKeeper变更ISR。

 **Broker故障恢复过程**

​    当Broker出现故障与ZooKeeper断开连接后，该Broker在ZooKeeper对应的znode会自动被删除，ZooKeeper会触发Controller注册在该节点的Watcher；Controller从ZooKeeper的/brokers/ids节点上获取宕机Broker上的所有Partition(简称set_p)；Controller再从ZooKeeper的/brokers/topics获取set_p中所有Partition当前的ISR；对于宕机Broker是Leader的Partition，Controller从ISR中选择幸存的Broker作为新Leader；最后Controller通过LeaderAndIsrRequest请求向set_p中的Broker发送LeaderAndISRRequest请求。

​    受到影响的Broker会收到Controller发送的LeaderAndIsrRequest请求后，Broker通过ReplicaManager的becomeLeaderOrFollower方法响应LeaderAndIsrRequest：新Leader会将HW更新为它的LEO值，而Follower则通过一系列策略截断log以保证数据一致性。发生故障后，由Controller负责选举受影响Partition的新Leader并通知到相关Broker，具体过程可参考下图。

#### 2.3.3.2. Controller故障

![1714399617953-34e106ad-b1d4-427a-943c-28cbb8ac9bd0.png](assets/1714399617953-34e106ad-b1d4-427a-943c-28cbb8ac9bd0.png)

**场景1 Controller与ZooKeeper断开连接**

此时ZooKeeper会将Controller临时节点删除，并按照下节的故障恢复过程重新竞选出新Controller。而原本的Controller由于无法连上ZooKeeper，它什么也执行不了；当它与ZooKeeper恢复连接后发现自己不再是Controller，会在Kafka集群中充当一个普通的Broker。

**场景2 Controller与某个Broker断开连接**

因为Controller无法通知到Broker0，所以Broker0不晓得Partition0的Leader已经更换了，所以也会出现3.1.1节场景2描述的出现短暂服务不可用并可能发生数据丢失。

**Controller故障恢复过程**

最后，集群中的Controller也会出现故障，因此Kafka让所有Broker都在ZooKeeper的Controller节点上注册一个Watcher。Controller发生故障时对应的Controller临时节点会自动删除，此时注册在其上的Watcher会被触发，所有活着的Broker都会去竞选成为新的Controller(即创建新的Controller节点，由ZooKeeper保证只会有一个创建成功)。竞选成功者即为新的Controller，会在ZooKeeper的下述节点上注册Watcher，以监控各Broker运行状态、负责Leader宕机的失败恢复，并对管理脚本做出响应。

- 在/admin节点上注册Watcher，以应对管理员脚本对Topic及Partition的影响；
- 在/brokers/ids节点上注册Watcher，以获取各Brokers的状态变化；
- 在/brokers/topics节点上注册Watcher，以监控每个Partition的ISR副本状态；

## 2.4. 高性能

Producer生产消息会涉及大量的消息网络传输，如果Producer每生产一个消息就发送到Broker会造成大量的网络消耗，严重影响到Kafka的性能。为了解决这个问题，Kafka使用了批量发送的方式，Broker在持久化消息，读取消息的时候，如果采用传统的IO读写方式，会严重影响Kafka的性能，为了解决这个问题，Kafka采用了顺序写+零拷贝的方式。下面分别**从批量发送消息，持久化消息，零拷贝**三个角度介绍Kafka如何提高性能。

### 2.4.1. 批量发送消息

Producer生成消息发送到Broker，涉及到大量的网络传输，如果一次网络传输只发送一条消息，会带来严重的网络耗时，为了解决这个问题，Kafka采用批量发送的方式。下面介绍Producer生产消息发送到Broker的过程。

#### 2.4.1.1. Partition

kafka的消息是一个一个的键值对，键可以设置为默认的null，键有两个用途，可以作为消息的附加信息，也可以用来决定该消息被写入到哪个partition。Topic的数据被分为一个或者多个Partition，Partition是消息的集合，Partition是Consumer消费的最小粒度。

![image-20240620151935050](assets/image-20240620151935050.png)

Kafka通过将Topic划分为多个Partition，Producer将消息分发到多个本地Partition的消息队列中，每个Partition消息队列的消息会写入到不同的Leader节点，消息经过路由策略，被分发到不同的Partition对应的本地队列，然后再批量发送到Partition对应的Leader节点。

#### 2.4.1.2. 消息路由

Kafka中Topic中有多个partition，那么消息分配到某个Partition的策略称为路由策略，kafka的路由策略主要分为三种：

- Round Roibin：Producer将消息均衡的分配到各Partition本地队列上，是最常用的分区策略。
- 散列：kafka对消息的key进行散列，根据散列值将消息路由到特定的Partition上，键相同的消息总是被路由到相同的partition上。
- 自定义分区策略：kafka支持自定义分区策略，可以将某一系列的消息映射到相同的Partition。

#### 2.4.1.3. 发送流程

#### ![1714442198025-4cc058b7-68dc-4afe-82be-1b9ac040686a.png](assets/1714442198025-4cc058b7-68dc-4afe-82be-1b9ac040686a.png)

Producer先生产消息、序列化消息并压缩消息后，追加到本地的记录收集器(RecordAccumulator)，Sender不断轮询记录收集器，当满足一定条件时，将队列中的数据发送到Partition Leader节点。Sender发送数据到Broker的条件有两个：

- 消息大小达到阈值
- 消息等待发送的时间达到阈值

**Producer会为每个Partition都创建一个双端队列来缓存客户端消息，队列的每个元素是一个批记录(ProducerBatch)，批记录使用createdMs表示批记录的创建时间(批记录中第一条消息加入的时间)， topicPartion表示对应的Partition元数据。当Producer生产的消息经过序列化，会被先写入到recordsBuilder对象中。一旦队列中有批记录的大小达到阈值，就会被Sender发送到Partition对应的Leader节点；若批记录等待发送的时间达到阈值，消息也会被发送到Partition对应的Leader节点中**。

![1714443264886-6a3e1f1b-4e7c-4a48-a3a7-1cffcb5c9cf2.png](assets/1714443264886-6a3e1f1b-4e7c-4a48-a3a7-1cffcb5c9cf2.png)

追加消息时首先要获取Partition所属的队列，然后取队列中最后一个批记录，如果队列中不存在批记录或者批记录的大小达到阈值，应该创建新的批记录，并且加入队列的尾部。这里先创建的批记录最先被消息填满，后创建的批记录表示最新的消息，追加消息时总是往队列尾部的批记录中追加。记录收集器用来缓存客户端的消息，还需要通过Sender才能将消息发送到Partition对应的Leader节点。

Sender读取记录收集器，得到每个Leader节点对应的批记录列表，找出准备好的Broker节点并建立连接，然后将各个Partition的批记录发送到Leader节点。具体的步骤如下：

- 消息被记录收集器收集，并按照Partition追加到队列尾部一个批记录中。 
- Sender通过ready()从记录收集器中找出已经准备好的服务端节点，规则是Partition等待发送的消息大小和等待发送的时间达到阈值。
- 节点已经准备好，如果客户端还没有和它们建立连接，通过connect()建立到服务端的连接。
- Sender通过drain()从记录收集器获取按照节点整理好的每个Partition的批记录。
- Sender得到每个节点的批记录后，为每个节点创建客户端请求，并将消息发送到服务端。

### 2.4.2. 消息持久化

#### 2.4.2.1. 随机IO和顺序IO

磁盘上的数据由柱面号，盘片号，扇区号标识，当需要从磁盘读数据时，系统会将数据逻辑地址传给磁盘，磁盘的控制电路按照寻址逻辑地址翻译为物理地址，即确定要读的数据在哪个磁道哪个扇区。

为了实现读取这个扇区的数据，需要将磁头放到这个扇区上面，为了实现这一点：

- 首先必须找到柱面，即磁头需要移动对准相应磁道，这个过程叫做寻址或者定位
- 盘面确定后，盘片开始旋转，将目标扇区旋转到磁头下

因此，一次读数据请求完成过程由三个动作组成：

- 寻道：磁头移动定位到指定磁道，这部分时间代价最高，最大可达0.1s左右
- 旋转延迟：等待指定扇区旋转至磁头下，与硬盘自身性能有关，xxxx转/分
- 数据传输：数据通过总线从磁盘传送到内存的时间。

对于从磁盘中读取数据的操作叫做IO操作，这里由两种情况：

- 假设我们所需要的数据是随机分散在磁盘的不同盘片的不同扇区中，那么找到相应的数据需要等到磁臂通过寻址作用旋转到指定的盘片，然后盘片寻找到对应的扇区，才能找到我们所需要的一块数据，一次进行此过程直到找到所有数据，称为随机ID，读取数据速度较慢。
- 假设我们已经找到了第一块数据，并且其他所有数据就在这一块数据后面，那么就不需要重新寻址，可以依次拿到我们所需要的数据，称为顺序IO。

顺序IO相对于随机IO，减少了大量的磁盘寻址过程，提高了数据查询效率。

#### 2.4.2.2. Broker写消息

Broker中需要将大量的消息做持久化，而且存在大量的消息查询场景，如果采用传统的IO操作，会带来大量的磁盘寻址，影响消息查询的速度，限制了Kafka的性能，为了解决这个问题，Kafka采用顺序写的方式来做消息持久化。

Producer传递到Broker的消息集中的每条消息都会分配一个顺序值，用来表示Producer所生产消息的顺序，每一批的顺序值都是从0开始的，假设Producer写到partition的消息由3条，对应的顺序为0，1，2。Producer创建的消息集中每条消息的顺序只是相对于本批次的序号，所有这个值不能直接存储在日志文件中，服务端会将每条消息的顺序值转为绝对偏移量（Broker从Partition维度来标记消息的顺序，用于控制Consumer消费消息的顺序）。Kafka通过nexOffset（下一个偏移量）来记录存储在日志中最近一条消息的偏移量。

 Broker将每个Partition的消息追加到日志中，是以日志分段(Segment)为单位的。当Segment的大小达到阈值(默认是1G)时，会新创建一个Segment保存新的消息，每个Segment都有一个基准偏移量(baseOffset，每个Segment保存的第一个消息的绝对偏移量)，通过这个基准偏移量，就可以计算出每条消息在Partition中的绝对偏移量。 每个日志分段由数据文件和索引文件组，数据文件(文件名以log结尾)保存了消息集的具体内容，索引文件(文件名以index结尾)保存了消息偏移量到物理位置的索引。Broker中通过下一个偏移量元数据（nextOffsetMetaData），指定当前写入日志消息的起始偏移量，在追加消息后，更新nextOffsetMetaData，作为下一批消息的起始偏移量。

nextOffsetMetaData的读写操作发生在持久化和读取消息中，具体流程如下所示：

1、Producer发送消息集到Broker，Broker将这一批消息追加到日志；

2、每条消息需要指定绝对偏移量，Broker会用nextOffsetMetaData的值作为起始偏移值；

3、Broker将每条带有偏移量的消息写入到日志分段中；

4、Broker获取这一批消息中最后一条消息的偏移量，加1后更新nextOffsetMetaData；

5、Consumer根据这个变量的最新值拉取消息。一旦这个值发生变化，Consumer就能拉取到新写入的消息。

由于写入到日志分段中的消息集，都是以nextOffsetMetaData作为起始的绝对偏移量。因为这个起始偏移量总是递增，所以每一批消息的偏移量也保持递增，而且每一个Partition的所有日志分段中，所有消息的偏移量都是递增。如下图所示，新创建日志分段的基准偏移量，比之前的分段的基准偏移量要大，同一个日志分段中，新消息的偏移量也比之前消息的偏移量要大。

建立索引文件的目的：快速定位指定偏移量消息在数据文件中的物理位置，其中索引文件保存的是一部分消息的相对偏移量到物理地址的映射，使用相对偏移量而不是绝对偏移量是为了节约内存。

#### 2.4.2.3. 基于索引文件的查询

![img](assets/1714446709472-f4efce23-d4e4-4008-bdc9-15f15c3a92d9.png)

Kafka通过索引文件提高对磁盘上消息的查询效率。假设有1000条消息，每100条消息写满了一个日志分段，一共会有10个日志分段。客户端要查询偏移量为938的消息内容，如果没有索引文件，我们必须从第一个日志分段的数据文件中，从第一条消息一直往前读，直到找到偏移量为999的消息。有了索引文件后，我们可以在最后一个日志分段的索引文件中，首先使用绝对偏移量999减去基准偏移量900得到相对偏移量99，然后找到最接近相对偏移量99的索引数据90，相对偏移量90对应的物理地址是1365，然后再到数据文件中，从文件物理位置1365开始往后读消息，直到找到偏移量为999的消息。

Kafka的索引文件的特性：

- 索引文件映射偏移量到文件的物理位置，它不会对每条消息都建立索引，所以是稀疏的。
- 索引条目的偏移量存储的是相对于“基准偏移量”的“相对偏移量” ，不是消息的“绝对偏移量” 。
- 偏移量是有序的，查询指定的偏移量时，使用二分查找可以快速确定偏移量的位置。
- 指定偏移量如果在索引文件中不存在，可以找到小于等于指定偏移量的最大偏移量。
- 稀疏索引可以通过内存映射方式，将整个索引文件都放入内存，加快偏移量的查询。

**由于Broker是将消息持久化到当前日志的最后一个分段中，写入文件的方式是追加写，采用了对磁盘文件的顺序写。对磁盘的顺序写以及索引文件加快了Broker查询消息的速度。**

#### 2.4.2.4. 零拷贝

Kafka中存在大量的网络数据持久化到磁盘(Producer到Broker)和磁盘文件通过网络发送(Broker到Consumer)的过程。这一过程的性能直接影响到Kafka的整体性能。Kafka采用零拷贝这一通用技术解决该问题。

零拷贝技术可以减少数据拷贝和共享总线操作的次数，消除传输数据在存储器之间不必要的中间拷贝次数，减少用户应用程序地址空间和操作系统内核地址空间之间因为上下文切换而带来的开销，从而有效地提高数据传输效率。 

以将磁盘文件通过网络发送为例。下面展示了传统方式下读取数据后并通过网络发送所发生的数据拷贝：

![1714447184098-21c242e1-3f3f-45b6-b11a-af01996964e9.png](assets/1714447184098-21c242e1-3f3f-45b6-b11a-af01996964e9.png)



Linux 2.4+内核通过sendfile系统调用，提供了零拷贝，数据通过DMA拷贝到内核态buffer后，CPU 把内核缓冲区中的文件描述符信息（包括内核缓冲区的内存地址和偏移量）发送到 socket 缓冲区，直接通过DMA拷贝到NIC buffer，无需CPU拷贝。除了减少数据拷贝外， 因为整个读文件-网络发送由一个sendfile调用完成，整个过程只有两次上下文切换，没有CPU数据拷贝，因此大大提高了性能。

![1714447585485-920f1dd3-88f2-4741-8ca7-2e36aeef53e0.png](assets/1714447585485-920f1dd3-88f2-4741-8ca7-2e36aeef53e0.png)

- sendfile()通过DMA将文件内容拷贝到一个读取缓冲区，然后由内核将数据拷贝到与输出套接字相关联的内核缓冲区。
- 用户进程发起 sendfile 系统调用，上下文（切换 1）从用户态转向内核态
- DMA 控制器，把数据从硬盘中拷贝到内核缓冲区。
- CPU 将读缓冲区中数据拷贝到 socket 缓冲区
- DMA 控制器，异步把数据从 socket 缓冲区拷贝到网卡，
- 上下文（切换 2）从内核态切换回用户态，sendfile 调用返回。

从具体实现来看，Kafka的数据传输通过TransportLayer来完成，其子类PlaintextTransportLayer通过Java NIO的FileChannel的transferTo()和transferFrom()方法实现零拷贝。transferTo()和transferFrom()并不保证一定能使用零拷贝，实际上是否能使用零拷贝与操作系统相关，如果操作系统提供sendfile这样的零拷贝系统调用，则这两个方法会通过这样的系统调用充分利用零拷贝的优势，否则并不能通过这两个方法本身实现零拷贝。

## 2.5 幂等消息和事务消息

**所谓的消息交付可靠性保障，是指 Kafka 对 Producer 和 Consumer 要处理的消息提供什么样的承诺。**常见的承诺有以下三种：

- 最多一次（at most once）：消息可能会丢失，但绝不会被重复发送：
- 至少一次（at least once）：消息不会丢失，但有可能被重复发送。
- 精确一次（exactly once）：消息不会丢失，也不会被重复发送（通过幂等性和事务性来实现）。

### 2.5.1 幂等消息

- 是 0.11.0.0 版本引入的新功能。

- 指定幂等消息：enable.idempotence 被设置成 true 后，Producer 自动升级成幂等性 Producer，其他所有的代码逻辑都不需要改变。Kafka 自动帮你做消息的重复去重。

  ```java
  props.put(“enable.idempotence”, ture);
  // 或者
  props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG， true)。
  ```

- 底层具体的原理很简单，就是经典的用空间去换时间的优化思路，即在 Broker 端多保存一些字段。当 Producer 发送了具有相同字段值的消息后，Broker 能够自动知晓这些消息已经重复了，于是可以在后台默默地把它们“丢弃”掉。当然，实际的实现原理并没有这么简单，但你大致可以这么理解。
- 作用范围：一个幂等性 Producer 能够保证某个主题的一个分区上不出现重复消息，它无法实现多个分区的幂等性。幂等性 Producer 只能实现单会话上的幂等性，不能实现跨会话的幂等性。这里的会话，你可以理解为 Producer 进程的一次运行。当你重启了 Producer 进程之后，这种幂等性保证就丧失了。

**具体实现原理：**

- 幂等键
  1.  **Producer ID（PID）** Kafka为每个生产者实例分配一个全局唯一的PID。这个PID在整个Kafka集群中是独一无二的，用于标识特定的生产者实例。PID的分配是在生产者实例首次连接到Kafka集群时进行的，并且这个ID会一直保持不变，直到生产者实例关闭或断开连接。 
  2.  **序列号（Sequence Number）** 除了PID之外，生产者还会为它发送的每条消息分配一个递增的序列号。这个序列号是在该生产者实例的生命周期内单调递增的，确保每条消息都有一个唯一的序列号。即使两条消息的内容完全相同，只要它们的序列号不同，它们就被视为不同的消息。 
  3.  **PID和序列号的组合** PID和序列号一起构成了一个独特的组合，这个组合可以作为每条消息的唯一标识。Kafka Broker使用这个组合来判断是否已经处理过该消息。当Broker接收到一条消息时，它会检查该PID和序列号是否已经在内部缓存中存在。
- 缓存机制
  -  Kafka Broker为每个PID维护一个缓存区域，主要用于存储最近一段时间内接收到的消息序列号。这个缓存区域是一个数据结构（如哈希表或有序集合），它允许Broker快速地根据PID和序列号来检查消息是否已经被处理过。缓存区域的大小和过期策略可以根据需要进行配置，以平衡内存使用和消息去重的准确性。
  - 当Broker接收到一个新的消息时，它会首先根据PID查找到对应的缓存区域。然后，Broker会检查该消息的序列号是否已经在缓存中存在。这个检查过程通常是高效的，因为缓存区域是专为快速查找而设计的。
  -  如果消息的序列号在缓存中已经存在，这意味着之前已经有一个具有相同PID和序列号的消息被处理过。因此，这条新消息实际上是一个重复的消息。为了避免重复处理，Broker会拒绝这条消息的写入请求，即不会将其追加到日志中。
  -  如果消息的序列号在缓存中不存在，那么这条消息就是一个新的、未被处理过的消息。Broker会将该消息的序列号加入缓存区域，并继续处理该消息，包括将其追加到日志中、更新索引等。
  - 随着时间的推移，缓存区域中的序列号会逐渐增多。为了保持缓存的高效性和准确性，Kafka可能会采取一些策略来管理缓存，比如定期清理过期的序列号（即已经很久没有被使用过的序列号）或限制缓存的大小。

### 2.5.2 事务消息

- 事务型 Producer 能够保证将消息原子性地写入到多个分区中。这批消息要么全部写入成功，要么全部失败。另外，事务型 Producer 也不惧进程的重启。Producer 重启回来后，Kafka 依然保证它们发送消息的精确一次处理。

- 设置事务型 Producer 的方法也很简单，满足两个要求即可：

  - 和幂等性 Producer 一样，开启 enable.idempotence = true。
  - 设置 Producer 端参数 transctional. id。最好为其设置一个有意义的名字。

  ```java
  // 事务的初始化
  producer.initTransactions();
  try {
      // 事务的开始
      producer.beginTransaction();
      producer.send(record1);
      producer.send(record2);
      // 事务的提交
      producer.commitTransaction();
  } catch (KafkaException e) {
      // 事务的终止
      producer.abortTransaction();
  }
  ```

- 这段代码能够保证 Record1 和 Record2 被当作一个事务统一提交到 Kafka，要么它们全部提交成功，要么全部写入失败。实际上即使写入失败，Kafka 也会把它们写入到底层的日志中，也就是说 Consumer 还是会看到这些消息。因此在 Consumer 端，读取事务型 Producer 发送的消息也是需要一些变更的。修改起来也很简单，设置 isolation.level 参数的值即可。当前这个参数有两个取值：

  1. read_uncommitted：这是默认值，表明 Consumer 能够读取到 Kafka 写入的任何消息，不论事务型 Producer 提交事务还是终止事务，其写入的消息都可以读取。很显然，如果你用了事务型 Producer，那么对应的 Consumer 就不要使用这个值。
  2. read_committed：表明 Consumer 只会读取事务型 Producer 成功提交事务写入的消息。当然了，它也能看到非事务型 Producer 写入的所有消息。 





## 2.5. Kafka的一些坑

### 2.5.1. 消息积压

**现象**：在使用MQ过程中由于种种原因导致消息消费不及时导致大量消息积压

**原因**：

- 消费流程卡死
- 消息消费耗时过长
- 消费组客户端启动失败
- 消费线程过少，消费能力不够
- 客户端在消费失败后设置 return Consume_FAILURE 一旦不能恢复会一直重试

**解决方案：**

- 消费逻辑的业务处理尽量时间不要太长，如果存在长耗时逻辑尽量异步处理
- 不要过多的和外系统服务进行交互，避免其他服务问题导致消费能力下降
- 消费线程要对异常进行分类处理，不要发生异常轻易终止或者关闭消费节点的注册。
- 对于单partition消息消费在不需要保证有序的情况下开启并行消息
- 发现问题及时扩容partition并扩容消费者机器。
- 消费失败不要使用Consume_FAILURE,可以使用RECONSUMER_LATER,最好做好备份逻辑。

### 2.5.2. 消息丢失

**现象**：在MQ使用过程中由于MQ系统故障或者使用不当导致消息丢失

- **生产者丢失消息**：调用`send`方法发送消息之后，消息可能因为网络问题并没有发送过去。
  - 不要使用 producer.send(msg)，而要使用 producer.send(msg, callback)。记住，一定要使用带有回调通知的 send 方法。


```java
//1. 可以通过 `get()`方法获取调用结果，但是这样也让它变为了同步操作
SendResult<String, Object> sendResult = kafkaTemplate.send(topic, o).get();
if (sendResult.getRecordMetadata() != null) {
  logger.info("生产者成功发送消息到" + sendResult.getProducerRecord().topic() + "-> " + sendRe
              sult.getProducerRecord().value().toString());
}        
// 2. 添加回调函数的形式
ListenableFuture<SendResult<String, Object>> future = kafkaTemplate.send(topic, o);
        future.addCallback(result -> logger.info("生产者成功发送消息到topic:{} partition:{}的消息", result.getRecordMetadata().topic(), result.getRecordMetadata().partition()),
                ex -> logger.error("生产者发送消失败，原因：{}", ex.getMessage()));

```

- **消费者丢失消息**：当消费者拉取到了分区的某个消息之后，消费者会自动提交了 offset。自动提交的话会有一个问题，试想一下，当消费者刚拿到这个消息准备进行真正消费的时候，突然挂掉了，消息实际上并没有被消费，但是 offset 却被自动提交了。
  - 确保消息消费完成再提交。Consumer 端有个参数 enable.auto.commit，最好把它设置成 false，并采用手动提交位移的方式。就像前面说的，这对于单 Consumer 多线程处理的场景而言是至关重要的。 但是，这样会带来消息被重新消费的问题。比如你刚刚消费完消息之后，还没提交 offset，结果自己挂掉了，那么这个消息理论上就会被消费两次。
- **kafka弄丢了消息**：假如 leader 副本所在的 broker 突然挂掉，那么就要从 follower 副本重新选出一个 leader ，但是 leader 的数据还有一些没有被 follower 副本的同步的话，就会造成消息丢失。
  - 解决办法就是我们设置 **acks = all**。acks 是 Kafka 生产者(Producer) 很重要的一个参数。
  - 设置 unclean.leader.election.enable = false。这是 Broker 端的参数，它控制的是哪些 Broker 有资格竞选分区的 Leader。如果一个 Broker 落后原先的 Leader 太多，那么它一旦成为新的 Leader，必然会造成消息的丢失。
  - 设置 replication.factor >= 3。这也是 Broker 端的参数。其实这里想表述的是，最好将消息多保存几份，毕竟目前防止消息丢失的主要机制就是冗余。
  - 设置 min.insync.replicas > 1。这依然是 Broker 端参数，控制的是消息至少要被写入到多少个副本才算是“已提交”。设置成大于 1 可以提升消息持久性。在实际环境中千万不要使用默认值 1。

### 2.5.3. 重复消费 

现象：在使用MQ的过程中经常会遇到消息被重复消费的问题

原因：

- 绝大部分中间件均不能保证消息只被消费一次
- 生产者重复生产消息

解决：

- 消费消息要严格幂等控制

### 2.5.4. 消息发送失败

现象：在MQ使用过程中会遇到不规范或者系统故障导致消息发送失败

**原因：**

- 客户端使用不规范，重复创建实例，造成大量系统资源消耗
- 系统机场未能及时监控流量，没有限流，切流预案
- 未处理发送结果

**解决：**

- 按照规范创建客户端，可以采用spring bean配置创建，保证一个消费组或者生产者只有一个实例对象
- 关注发送结果
- 构建有效的流量监控应急预案

## 2.6. 面试题

### 2.6.1. Zookeeper 在 Kafka 中的作用是什么？

**Broker 注册**：在 Zookeeper 上会有一个专门**用来进行 Broker 服务器列表记录**的节点。每个 Broker 在启动时，都会到 Zookeeper 上进行注册，即到 `/brokers/ids` 下创建属于自己的节点。每个 Broker 就会将自己的 IP 地址和端口等信息记录到该节点中去

**Topic 注册**：在 Kafka 中，同一个**Topic 的消息会被分成多个分区**并将其分布在多个 Broker 上，**这些分区信息及与 Broker 的对应关系**也都是由 Zookeeper 在维护。比如我创建了一个名字为 my-topic 的主题并且它有两个分区，对应到 zookeeper 中会创建这些文件夹：`/brokers/topics/my-topic/Partitions/0`、`/brokers/topics/my-topic/Partitions/1`

**负载均衡**：上面也说过了 Kafka 通过给特定 Topic 指定多个 Partition, 而各个 Partition 可以分布在不同的 Broker 上, 这样便能提供比较好的并发能力。 对于同一个 Topic 的不同 Partition，Kafka 会尽力将这些 Partition 分布到不同的 Broker 服务器上。当生产者产生消息后也会尽量投递到不同 Broker 的 Partition 里面。当 Consumer 消费的时候，Zookeeper 可以根据当前的 Partition 数量以及 Consumer 数量来实现动态负载均衡。

### 2.6.2. 使用 Kafka 能否不引入 Zookeeper?

在 Kafka 2.8 之前，Kafka 最被大家诟病的就是其重度依赖于 Zookeeper。在 Kafka 2.8 之后，引入了基于 Raft 协议的 KRaft 模式，不再依赖 Zookeeper，大大简化了 Kafka 的架构，让你可以以一种轻量级的方式来使用 Kafka。

不过，要提示一下：**如果要使用 KRaft 模式的话，建议选择较高版本的 Kafka，因为这个功能还在持续完善优化中。Kafka 3.3.1 版本是第一个将 KRaft（Kafka Raft）共识协议标记为生产就绪的版本。**

### 2.6.2. Kafka 消费顺序、消息丢失和重复消费

- **如何保证消息顺序消费**

  - 1 个 Topic 只对应一个 Partition。
  - （推荐）发送消息的时候指定 key/Partition。

- **如何保证消息不丢失**

  - **生产者丢失消息**：调用`send`方法发送消息之后，消息可能因为网络问题并没有发送过去。
- 不要使用 producer.send(msg)，而要使用 producer.send(msg, callback)。记住，一定要使用带有回调通知的 send 方法。
  
  ```java
  //1. 可以通过 `get()`方法获取调用结果，但是这样也让它变为了同步操作
  SendResult<String, Object> sendResult = kafkaTemplate.send(topic, o).get();
  if (sendResult.getRecordMetadata() != null) {
    logger.info("生产者成功发送消息到" + sendResult.getProducerRecord().topic() + "-> " + sendRe
                sult.getProducerRecord().value().toString());
  }        
  // 2. 添加回调函数的形式
  ListenableFuture<SendResult<String, Object>> future = kafkaTemplate.send(topic, o);
          future.addCallback(result -> logger.info("生产者成功发送消息到topic:{} partition:{}的消息", result.getRecordMetadata().topic(), result.getRecordMetadata().partition()),
                  ex -> logger.error("生产者发送消失败，原因：{}", ex.getMessage()));
  


   **消费者丢失消息**：当消费者拉取到了分区的某个消息之后，消费者会自动提交了 offset。自动提交的话会有一个问题，试想一下，当消费者刚拿到这个消息准备进行真正消费的时候，突然挂掉了，消息实际上并没有被消费，但是 offset 却被自动提交了。**解决办法也比较粗暴，我们手动关闭自动提交 offset，每次在真正消费完消息之后再自己手动提交 offset 。**但是，细心的朋友一定会发现，这样会带来消息被重新消费的问题。比如你刚刚消费完消息之后，还没提交 offset，结果自己挂掉了，那么这个消息理论上就会被消费两次。
  - kafka弄丢了消息：假如 leader 副本所在的 broker 突然挂掉，那么就要从 follower 副本重新选出一个 leader ，但是 leader 的数据还有一些没有被 follower 副本的同步的话，就会造成消息丢失。解决办法就是我们设置 **acks = all**。acks 是 Kafka 生产者(Producer) 很重要的一个参数。

- **如何保证消息不重复消费**

  - 消费消息服务做幂等校验，比如 Redis 的 set、MySQL 的主键等天然的幂等功能。这种方法最有效。

### 2.6.3. Kafka 重试机制

- 在默认配置下，当消费异常会进行重试，重试多次后会跳过当前消息，继续进行后续消息的消费，不会一直卡在当前消息。下面是一段消费的日志，可以看出当 `test-0@95` 重试多次后会被跳过。因此，即使某个消息消费异常，Kafka 消费者仍然能够继续消费后续的消息，不会一直卡在当前消息，保证了业务的正常进行。

- Kafka 消费者在默认配置下**会进行最多 10 次 的重试，**每次重试的时间间隔为 0，即立即进行重试。如果在 10 次重试后仍然无法成功消费消息，则不再进行重试，消息将被视为消费失败。

- 当达到最大重试次数后，数据会直接被跳过，继续向后进行。当代码修复后，如何重新消费这些重试失败的数据呢？**死信队列（Dead Letter Queue，简称 DLQ）** 是消息中间件中的一种特殊队列。它主要用于处理无法被消费者正确处理的消息，通常是因为消息格式错误、处理失败、消费超时等情况导致的消息被"丢弃"或"死亡"的情况。当消息进入队列后，消费者会尝试处理它。如果处理失败，或者超过一定的重试次数仍无法被成功处理，消息可以发送到死信队列中，而不是被永久性地丢弃。在死信队列中，可以进一步分析、处理这些无法正常消费的消息，以便定位问题、修复错误，并采取适当的措施。

### 2.6.4. Kafka 和 RocketMQ的区别

RocketMQ参考了kafka的设计，同时又在kafka的基础上做了调整。

- 在架构上做了加法

  - **简化协调节点**：Kafka引入了zookeeper作为协调节点，RocketMQ简化了协调节点，将zookeeper去掉，换成了NameServer，用一种更轻量的方式管理队列的集群信息，不过Kafka在2.8.0去除了zookeeper，通过在broker之间加入一致性协议Raft.
  - **简化分区**：Kafka会将topic拆分为多个partation，用来提升并发性；RocketMQ将topic拆分为多个分区，然后名字换成了Queue，Kafka的partation会存放完整的消息，而RocketMQ的Queue却只存一些简要信息，比如消息偏移量offset，而消息的完整数据，则放到一个叫CommitLog的文件中，通过offset可以定位到CommitLog的某条消息。
    - 消费对比：Kafka消费消息，broker只需要直接从Partition上读取消息，而在roketMQ中，broker需要先从consumequeue上读取offset值，在到CommitLog上读取完整的数据。
  - **底层存储**：kafka的patation分区在底层有很多分段，每个段都可以认为是一个文件，对于每个段都是顺序写，对于多个topic的partation是随机写。Rocket对于单个broker上的多个topic上的数据全都写到一个逻辑文件CommitLog中，这就消除了随机写多文件的问题。大大提成了RocketMQ在多topic场景下的写性能。
  - **简化备份模型**：Kafka会将Partation分到多个broker中，并为partation配置副本，将Partation分为Leader和follower，主从partation之间会简历数据同步，RocketMQ 将Broker上所有的topic数据写到一个commitLog中，以Broker为单位分主从，保持高可用的同时，也大大简化了备份模型。
- 在功能上做了减法
  - **消息过滤**：Kafka支持通过topic将数据进行分类，比如订单数据和用户数据是两个不同的topic，但是不支持在同一个topic内进行数据分类，消费者需要消费topic中的所有消息，再进行过滤，而RocketMQ 支持给消息打上tag，消费者能根据tag过滤所需要的数据。
  - **支持事务**：Kafka只支持消息的事务，不支持自定义逻辑和发消息的事务，RocketMQ支持。
  - **延迟队列**：kafka不支持，但是Rocket支持（延迟队列）。
  - **死信队列**：Kafka原生不支持，需要自己实现，Rocket支持。
  - **消息回溯**：Kafka支持通过调整offset，让消费者从某个地方开始消费，而RocketMQ 除了可以调整offset，还支持调整时间（Kafka从0.10.0版本之后也支持了）。

RocketMQ 

![image-20240714153053078](assets/image-20240714153053078.png)

### 2.6.5. 如何使用Kafka使用延迟消息

1. 在发送延迟消息时不直接发送到目标topic，而是发送到一个用于处理延迟消息的topic，例如`delay-minutes-1`

2. 写一段代码拉取`delay-minutes-1`中的消息，将满足条件的消息发送到真正的目标主题里。

   1. KafkaConsumer 提供了暂停和恢复的API函数，调用消费者的暂停方法后就无法再拉取到新的消息，同时长时间不消费kafka也不会认为这个消费者已经挂掉了。另外为了能够更加优雅，我们会启动一个定时器来替换`sleep`。，完整流程如下图，当消费者发现消息不满足条件时，我们就暂停消费者，并把偏移量seek到上一次消费的位置以便等待下一个周期再次消费这条消息。
   2. 创建多个topic用于处理不同时间的延迟消息，例如`delay-minutes-1` `delay-minutes-5` `delay-minutes-10` `delay-minutes-15`以提供指数级别的延迟时间，这样比一个topic要好很多，毕竟在顺序拉取消息的时候，有一条消息不满足条件，后面的将全部进行排队。

   ![image-20240716221141641](assets/image-20240716221141641.png)

```java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.ExecutionException;

@SpringBootTest
public class DelayQueueTest {

    private KafkaConsumer<String, String> consumer;
    private KafkaProducer<String, String> producer;
    private volatile Boolean exit = false;
    private final Object lock = new Object();
    private final String servers = "";

    @BeforeEach
    void initConsumer() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, servers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "d");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
        props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, "5000");
        consumer = new KafkaConsumer<>(props, new StringDeserializer(), new StringDeserializer());
    }

    @BeforeEach
    void initProducer() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, servers);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producer = new KafkaProducer<>(props);
    }

    @Test
    void testDelayQueue() throws JsonProcessingException, InterruptedException {
        String topic = "delay-minutes-1";
        List<String> topics = Collections.singletonList(topic);
        consumer.subscribe(topics);

        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                synchronized (lock) {
                    consumer.resume(consumer.paused());
                    lock.notify();
                }
            }
        }, 0, 1000);

        do {

            synchronized (lock) {
                ConsumerRecords<String, String> consumerRecords = consumer.poll(Duration.ofMillis(200));

                if (consumerRecords.isEmpty()) {
                    lock.wait();
                    continue;
                }

                boolean timed = false;
                for (ConsumerRecord<String, String> consumerRecord : consumerRecords) {
                    long timestamp = consumerRecord.timestamp();
                    TopicPartition topicPartition = new TopicPartition(consumerRecord.topic(), consumerRecord.partition());
                    if (timestamp + 60 * 1000 < System.currentTimeMillis()) {

                        String value = consumerRecord.value();
                        ObjectMapper objectMapper = new ObjectMapper();
                        JsonNode jsonNode = objectMapper.readTree(value);
                        JsonNode jsonNodeTopic = jsonNode.get("topic");

                        String appTopic = null, appKey = null, appValue = null;

                        if (jsonNodeTopic != null) {
                            appTopic = jsonNodeTopic.asText();
                        }
                        if (appTopic == null) {
                            continue;
                        }
                        JsonNode jsonNodeKey = jsonNode.get("key");
                        if (jsonNodeKey != null) {
                            appKey = jsonNode.asText();
                        }

                        JsonNode jsonNodeValue = jsonNode.get("value");
                        if (jsonNodeValue != null) {
                            appValue = jsonNodeValue.asText();
                        }
                        // send to application topic
                        ProducerRecord<String, String> producerRecord = new ProducerRecord<>(appTopic, appKey, appValue);
                        try {
                            producer.send(producerRecord).get();
                            // success. commit message
                            OffsetAndMetadata offsetAndMetadata = new OffsetAndMetadata(consumerRecord.offset() + 1);
                            HashMap<TopicPartition, OffsetAndMetadata> metadataHashMap = new HashMap<>();
                            metadataHashMap.put(topicPartition, offsetAndMetadata);
                            consumer.commitSync(metadataHashMap);
                        } catch (ExecutionException e) {
                            consumer.pause(Collections.singletonList(topicPartition));
                            consumer.seek(topicPartition, consumerRecord.offset());
                            timed = true;
                            break;
                        }
                    } else {
                        consumer.pause(Collections.singletonList(topicPartition));
                        consumer.seek(topicPartition, consumerRecord.offset());
                        timed = true;
                        break;
                    }
                }

                if (timed) {
                    lock.wait();
                }
            }
        } while (!exit);

    }
}

```

