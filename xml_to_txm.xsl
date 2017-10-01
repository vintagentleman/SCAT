<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="w">
    <w>
      <xsl:for-each select="./@*">
        <xsl:attribute name="{name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>

      <xsl:choose>
        <!-- В тег - исправленный вариант, в атрибут - подстроку между угловыми скобками -->
        <xsl:when test="./orig/choice">
          <xsl:attribute name="reg">
            <xsl:value-of select="substring-before(substring-after(./reg, '&lt;'), '&gt;')"/>
          </xsl:attribute>
          <xsl:copy-of select="./orig/choice/corr/node()"/>
        </xsl:when>
        
        <!-- Стандартный случай с поправкой на правку -->
        <xsl:when test="./orig/sic">
          <xsl:attribute name="reg">
            <xsl:value-of select="./reg"/>
          </xsl:attribute>
          <xsl:copy-of select="./orig/sic/node()"/>
        </xsl:when>
        
        <!-- Стандартный случай -->
        <xsl:otherwise>
          <xsl:attribute name="reg">
            <xsl:value-of select="./reg"/>
          </xsl:attribute>
          <xsl:copy-of select="./orig/node()"/>
        </xsl:otherwise>
      </xsl:choose>
    </w>
  </xsl:template>
</xsl:stylesheet>
