<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="#all"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:xd="http://www.pnp-software.com/XSLTdoc"
  version="2.0">
    

  <xd:doc type="stylesheet">
    <xd:short>
      This stylesheet is designed for TXM XTZ import module to create 
      HTML editions of corpus texts. This stylesheet should be used at 
      "4-edition" step and must be accompanied by 1-default-html.xsl. 
      See TXM User Manual for more details 
      (http://textometrie.ens-lyon.fr/spip.php?rubrique64)
    </xd:short>
    <xd:detail>
      This software is dual-licensed:
      
      1. Distributed under a Creative Commons Attribution-ShareAlike 3.0
      Unported License http://creativecommons.org/licenses/by-sa/3.0/ 
      
      2. http://www.opensource.org/licenses/BSD-2-Clause
      
      All rights reserved.
      
      Redistribution and use in source and binary forms, with or without
      modification, are permitted provided that the following conditions are
      met:
      
      * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
      
      * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
      
      This software is provided by the copyright holders and contributors
      "as is" and any express or implied warranties, including, but not
      limited to, the implied warranties of merchantability and fitness for
      a particular purpose are disclaimed. In no event shall the copyright
      holder or contributors be liable for any direct, indirect, incidental,
      special, exemplary, or consequential damages (including, but not
      limited to, procurement of substitute goods or services; loss of use,
      data, or profits; or business interruption) however caused and on any
      theory of liability, whether in contract, strict liability, or tort
      (including negligence or otherwise) arising in any way out of the use
      of this software, even if advised of the possibility of such damage.
      
      $Id$
      
      This stylesheet is based on TEI processpb.xsl by Sebastian Rahtz 
      available at 
      https://github.com/TEIC/Stylesheets/blob/master/tools/processpb.xsl 
      
      and is adapted by Alexei Lavrentiev to split an HTML edition for 
      TXM platform.
    </xd:detail>
    <xd:author>Sebastian Rahtz and Alexei Lavrentiev alexei.lavrentev@ens-lyon.fr</xd:author>
    <xd:copyright>2017, CNRS / UMR 5317 IHRIM (CACTUS research group)</xd:copyright>
  </xd:doc>

  <!--

  -->
  <xsl:output indent="no" method="html"/>
  
  <xsl:param name="css-name-txm">txm</xsl:param>
  <xsl:param name="css-name"><xsl:value-of select="$current-corpus-name"/></xsl:param>
  <xsl:param name="edition-name">default</xsl:param>
  <xsl:param name="number-words-per-page">999999</xsl:param>
  <xsl:param name="pagination-element">a[@class='txm-page']</xsl:param>
  <xsl:param name="output-directory"><xsl:value-of select="concat($current-file-directory,'/',$edition-name)"/></xsl:param>
  
  <xsl:variable name="current-file-name">
    <xsl:analyze-string select="document-uri(.)" regex="^(.*)/([^/]+)\.[^/]+$">
      <xsl:matching-substring>
        <xsl:value-of select="regex-group(2)"/>
      </xsl:matching-substring>
    </xsl:analyze-string>
  </xsl:variable>
  
  <xsl:variable name="current-file-directory">
    <xsl:analyze-string select="document-uri(.)" regex="^(.*)/([^/]+)\.[^/]+$">
      <xsl:matching-substring>
        <xsl:value-of select="regex-group(1)"/>
      </xsl:matching-substring>
    </xsl:analyze-string>
  </xsl:variable>
  
  <xsl:variable name="current-corpus-name">
    <xsl:analyze-string select="$current-file-directory" regex="^(.*)/([^/]+)/[^/]+$">
      <xsl:matching-substring>
        <xsl:value-of select="regex-group(2)"/>
      </xsl:matching-substring>
    </xsl:analyze-string>
  </xsl:variable>
  
  
  <xsl:template match="html/body">
    <xsl:variable name="pages">
      <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:apply-templates
          select="*|processing-instruction()|comment()|text()"/>
      </xsl:copy>
    </xsl:variable>
    <xsl:for-each select="$pages">
      <xsl:apply-templates  mode="pass2"/>
    </xsl:for-each>
    <!-- creating title page with metadata -->
  </xsl:template>
  
  
  <!-- first (recursive) pass. look for <pb> elements and group on them -->
  <xsl:template match="comment()|@*|processing-instruction()|text()">
    <xsl:copy-of select="."/>
  </xsl:template>
  
  <xsl:template match="*">
    <xsl:call-template name="checkpb">
      <xsl:with-param name="eName" select="local-name()"/>
    </xsl:call-template>
  </xsl:template>
  
  <xsl:template match="a[@class='txm-page']">
    
    <!--    <xsl:variable name="next-word-position" as="xs:integer">
      <xsl:choose>
        <xsl:when test="following::span[@class='w']">
          <xsl:value-of select="count(following::span[@class='w'][1]/preceding::span[@class='w'])"/>
        </xsl:when>
        <xsl:otherwise>20</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:variable name="next-pb-position" as="xs:integer">
      <xsl:choose>
        <xsl:when test="following::a[@class='txm-page']">
          <xsl:value-of select="count(following::a[@class='txm-page'][1]/preceding::span[@class='w'])"/>
        </xsl:when>
        <xsl:otherwise>999999999</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <!-\-<xsl:value-of select="count(following::a[@class='txm-page'][1]/preceding::a[@class='w'])"/>-\->
    <xsl:variable name="next-word-id">
      <xsl:choose>
        <xsl:when test="$next-pb-position - $next-word-position = 999999999"><!-\-w_0-\-><xsl:value-of select="concat($next-pb-position,' - ',$next-word-position)"/></xsl:when>
        <xsl:when test="$next-pb-position &gt; $next-word-position"><xsl:value-of select="following::*:span[@class='w'][1]/@id"/></xsl:when>
        <xsl:otherwise><!-\- w_0 -\-><xsl:value-of select="concat($next-pb-position,' - ',$next-word-position)"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>-->
    
    
    <!--  <a xmlns="http://www.w3.org/1999/xhtml">  -->
    
    <a>
      <xsl:copy-of select="@*"/>
      <!--<xsl:attribute name="next-word-id"><xsl:value-of select="$next-word-id"/></xsl:attribute>-->
    </a>
  </xsl:template>
  
  <xsl:template name="checkpb">
    <xsl:param name="eName"/>
    <xsl:choose>
      <xsl:when test="not(.//a[@class='txm-page'])">
        <xsl:copy-of select="."/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="pass">
          <xsl:call-template name="groupbypb">
            <xsl:with-param name="Name" select="$eName"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:for-each select="$pass">
          <xsl:apply-templates/>
        </xsl:for-each>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <xsl:template name="groupbypb">
    <xsl:param name="Name"/>
    <xsl:for-each-group select="node()" group-starting-with="a[@class='txm-page']">
      <xsl:choose>
        <xsl:when test="self::a[@class='txm-page']">
          <xsl:copy-of select="."/>
          <xsl:element name="{$Name}">
            <xsl:attribute name="rend">CONTINUED</xsl:attribute>
            <xsl:apply-templates select="current-group() except ."/>
          </xsl:element>
        </xsl:when>
        <xsl:otherwise>
          <xsl:element name="{$Name}">
            <xsl:for-each select="..">
              <xsl:copy-of select="@*"/>
              <xsl:apply-templates select="current-group()"/>
            </xsl:for-each>
          </xsl:element>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each-group>
  </xsl:template>
  
  <!-- second pass. group by <pb> (now all at top level) and wrap groups
       in <page> -->
  <xsl:template match="*" mode="pass2">
    <xsl:copy>
      <xsl:apply-templates select="@*|*|processing-instruction()|comment()|text()" mode="pass2"/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="comment()|@*|processing-instruction()|text()" mode="pass2">
    <xsl:copy-of select="."/>
  </xsl:template>
  
  
  
  <!--	<xsl:variable name="style">
	  <xsl:copy-of select="/html/head[1]/style[1]"></xsl:copy-of>
	</xsl:variable>-->
  
  <xsl:template match="*[a[@class='txm-page']]" mode="pass2" >    
    
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:for-each-group select="*" group-starting-with="a[@class='txm-page']">
        <xsl:choose>
          <xsl:when test="self::a[@class='txm-page']">
            <xsl:comment> Page <xsl:value-of select="@title"/> déplacée vers <xsl:value-of select="concat($output-directory,'/',$current-file-name,'_',@title,'.html')"/></xsl:comment>
            <xsl:result-document href="{$output-directory}/{$current-file-name}_{@title}.html/">
              <html>
                <head>
                  <meta name="txm:first-word-id" content="{@next-word-id}"/>
                  <title><xsl:value-of select="concat($current-file-name,', Page ',@title)"/></title>
                  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
                  <link rel="stylesheet" media="all" type="text/css" href="css/{$css-name-txm}.css"/>
                  <xsl:if test="matches($css-name,'\S')"><link rel="stylesheet" media="all" type="text/css" href="css/{$css-name}.css"/></xsl:if>
                  <!--<xsl:copy-of select="$style"/>-->
                </head>
                <body>
                  <div class="txmeditionpage">
                    <xsl:copy-of select="current-group() except ."/>
                  </div>
                </body>
              </html>
            </xsl:result-document>
            
          </xsl:when>
          <xsl:otherwise>
            <xsl:copy-of select="current-group()"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each-group>
    </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>
