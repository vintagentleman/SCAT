<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="l">
    <xsl:apply-templates/>
    <lb>
      <xsl:attribute name="n">
        <xsl:value-of select="@n"/>
      </xsl:attribute>
    </lb>
  </xsl:template>

  <xsl:template match="w">
    <w>
      <xsl:for-each select="./@*">
        <xsl:attribute name="{name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>

      <xsl:attribute name="src">
        <xsl:value-of select="./src"/>
      </xsl:attribute>
      <xsl:attribute name="reg">
        <xsl:value-of select="./reg"/>
      </xsl:attribute>

      <xsl:choose>
        <xsl:when test="./orig/choice">
          <xsl:value-of select="./orig/choice/corr"/>
        </xsl:when>
        <xsl:when test="./orig/sic">
          <xsl:value-of select="./orig/sic"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="./orig"/>
        </xsl:otherwise>
      </xsl:choose>
    </w>
  </xsl:template>
</xsl:stylesheet>
