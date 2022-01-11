import requests
"""
1:根据首页中的css中，获取其中的woff字体文件。
2：以其中的一个字体文件为例，建立映射关系
    ①uniefba与uniecbf肃然不一样，但是却描述了同一个字符（注意：不能用点的数量来判断是不是描述的同一个字符，只有起止点和点坐标完全一样的，才是描述同一个字符）
	如：
	uniefba：
	<TTGlyph name="uniefba" xMin="0" yMin="-14" xMax="550" yMax="728">
      <contour>
        <pt x="307" y="728" on="1"/>
        <pt x="205" y="728" on="0"/>
        <pt x="142" y="670" on="1"/>
        <pt x="76" y="612" on="0"/>
        <pt x="66" y="508" on="1"/>
        <pt x="147" y="508" on="1"/>
        <pt x="154" y="580" on="0"/>
        <pt x="236" y="658" on="0"/>
		……
        <pt x="418" y="374" on="1"/>
        <pt x="535" y="414" on="0"/>
        <pt x="535" y="534" on="1"/>
        <pt x="535" y="624" on="0"/>
        <pt x="410" y="728" on="0"/>
      </contour>
      <instructions/>
    </TTGlyph>
	
	uniecbf：
	    <TTGlyph name="uniecbf" xMin="0" yMin="-14" xMax="550" yMax="728">
      <contour>
        <pt x="307" y="728" on="1"/>
        <pt x="205" y="728" on="0"/>
        <pt x="142" y="670" on="1"/>
        <pt x="76" y="612" on="0"/>
        <pt x="66" y="508" on="1"/>
        <pt x="147" y="508" on="1"/>
        <pt x="154" y="580" on="0"/>
        <pt x="236" y="658" on="0"/>
        <pt x="308" y="657" on="1"/>
        <pt x="378" y="658" on="0"/>
		……
        <pt x="481" y="355" on="0"/>
        <pt x="418" y="374" on="1"/>
        <pt x="535" y="414" on="0"/>
        <pt x="535" y="534" on="1"/>
        <pt x="535" y="624" on="0"/>
        <pt x="410" y="728" on="0"/>
      </contour>
      <instructions/>
    </TTGlyph>
	两者的内容是完全一样的，所以是描述同一个字符。
	知道了这个方法，那么如何建立映射？
	
	可以以字形数据建立映射：{'name':['uniefba','uniecbf'],'value':'0','hex':md5(content)} #因为字形数据多，以MD5值来区分唯一值,
	选择一个woff文件，……
	

"""
headers={
'User-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

resp=requests.get('https://www.dianping.com/shop/G4mmqiZrzgkpQZGY',headers=headers)
print(resp.text)