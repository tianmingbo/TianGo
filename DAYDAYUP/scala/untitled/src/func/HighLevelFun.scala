package func


object HighLevelFun {
  def main(args: Array[String]): Unit = {
    val serries = Seq(1, 5, 4)
    val func = (x: Int) => x * 2
    var newSalaries = serries.map(func)
    println(newSalaries)
    newSalaries = serries.map(_ * 2) //作用同上
    println(newSalaries)
    val filter = (x: Int) => x % 2 == 0
    val newSalaries2 = serries.filter(filter)
    println(newSalaries)

    //返回函数的函数,(String, String) => String是返回一个参数为(String, String),返回一个String
    def urlBuilder(ssl: Boolean, domainName: String): (String, String) => String = {
      val schema = if (ssl) "https://" else "http://"
      (endpoint: String, query: String) => s"$schema$domainName/$endpoint?$query"
    }

    val domainName = "www.example.com"

    def getUrlFun: (String, String) => String = urlBuilder(ssl = true, domainName)

    val endpoint = "users"
    val query = "id=1"
    val url = getUrlFun(endpoint, query)
    println(url)
  }
}
