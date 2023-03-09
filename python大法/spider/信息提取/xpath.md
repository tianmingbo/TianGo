- 属性多值匹配
  //li[contains(@class,"li")]/a/text()

- 多属性匹配

  //li[contains(@class,"li") and @name='item']/a/text()  还支持其它运算符

- 按序选择
  //li[last()-2]/a/text()
  //li[position()<3]/a/text() 选择位置小于3的节点

- 节点轴选择
  //li[1]/ancestor::*  得到所有祖先节点
  //li[1]/ancestor::div 祖先中的div节点
  //li[1]/attribute::* 获取li的所有属性值
  //li[1]/child::a[@hred="baidu"] 获取子节点
  //li[1]/descendant::span 获取所有子孙节点
  //li[1]/following::*[2] 获取当前之后的所有节点
  //li[1]/following-sibling::* 获取当前之后的所有同级节点