<?xml version="1.0"?>
<xsl:stylesheet xmlns:edate="http://exslt.org/dates-and-times"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:tei="http://www.tei-c.org/ns/1.0" 
	xmlns:txm="http://textometrie.org/1.0"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:xd="http://www.pnp-software.com/XSLTdoc"
                exclude-result-prefixes="#all" version="2.0">
                
	<xd:doc type="stylesheet">
		<xd:short>
			This stylesheet is designed for TXM XTZ import module to create 
			HTML editions of corpus texts. This stylesheet should be used at 
			"4-edition" step and must be accompanied by 2-default-pager.xsl. 
			See TXM User Manual for more details 
			(http://textometrie.ens-lyon.fr/spip.php?rubrique64)
		</xd:short>
		<xd:detail>
			This stylesheet is free software; you can redistribute it and/or
			modify it under the terms of the GNU Lesser General Public
			License as published by the Free Software Foundation; either
			version 3 of the License, or (at your option) any later version.
			
			This stylesheet is distributed in the hope that it will be useful,
			but WITHOUT ANY WARRANTY; without even the implied warranty of
			MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
			Lesser General Public License for more details.
			
			You should have received a copy of GNU Lesser Public License with
			this stylesheet. If not, see http://www.gnu.org/licenses/lgpl.html
		</xd:detail>
		<xd:author>Alexei Lavrentiev alexei.lavrentev@ens-lyon.fr</xd:author>
		<xd:copyright>2017, CNRS / UMR 5317 IHRIM (CACTUS research group)</xd:copyright>
	</xd:doc>
                
                
                
	<xsl:output method="xml" encoding="UTF-8" omit-xml-declaration="no" indent="no"/>
	
	<!-- <xsl:output method="xml" encoding="UTF-8" omit-xml-declaration="no" indent="no"  doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/> -->
	
                
                <xsl:strip-space elements="*"/>
                
	<xsl:param name="pagination-element">pb</xsl:param>
	
	<xsl:variable name="word-element">
		<xsl:choose>
			<xsl:when test="//tei:c//txm:form">c</xsl:when>
			<xsl:otherwise>w</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<xsl:variable name="page-number-adjust" as="xs:integer">
		<xsl:choose>
			<xsl:when test="//tei:c//txm:form">1</xsl:when>
			<xsl:otherwise>2</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	

                <xsl:variable name="inputtype">
                	<xsl:choose>
                		<xsl:when test="//tei:w//txm:form">xmltxm</xsl:when>
                		<xsl:otherwise>xmlw</xsl:otherwise>
                	</xsl:choose>
                </xsl:variable>
	
	<xsl:variable name="filename">
		<xsl:analyze-string select="document-uri(.)" regex="^(.*)/([^/]+)\.[^/.]+$">
			<xsl:matching-substring>
				<xsl:value-of select="regex-group(2)"/>
			</xsl:matching-substring>
		</xsl:analyze-string>
	</xsl:variable>
                
                <xsl:template match="/">
                	<html>
                		<head>
                			<title><xsl:choose>
                				<xsl:when test="//tei:text/@id"><xsl:value-of select="//tei:text[1]/@id"/></xsl:when>
                				<xsl:otherwise><xsl:value-of select="$filename"/></xsl:otherwise>
                			</xsl:choose></title>
                			<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
                			<link rel="stylesheet" media="all" type="text/css" href="css/txm.css" />
                		</head>
                			<xsl:apply-templates select="descendant::tei:text"/>
                	</html>
                </xsl:template>

	<xsl:template match="tei:text">
		<body>
			<xsl:if test="$word-element='w'">
				<a class="txm-page" title="1"  next-word-id="w_0"/>
				<div class="metadata-page">
					<h1><xsl:value-of select="@id"></xsl:value-of></h1>
					<br/>
					<table>
						<xsl:for-each select="@*">
							<tr>
								<td><xsl:value-of select="name()"/></td>
								<td><xsl:value-of select="."/></td>
							</tr>
						</xsl:for-each>
					</table>
				</div>
				
			</xsl:if>
			<xsl:apply-templates/>
			
			<xsl:variable name="page_id"><xsl:value-of select="count(descendant::*[local-name()=$pagination-element])"/></xsl:variable>
			
			<xsl:if test="//tei:note[not(@place='inline') and not(matches(@type,'intern|auto'))][count(preceding::*[local-name()=$pagination-element]) = $page_id]">
				<xsl:text>&#xa;</xsl:text>
				<br/>
				<br/>			
				<span style="display:block;border-top-style:solid;border-top-width:1px;border-top-color:gray;padding-top:5px">                                                
					<xsl:for-each select="//tei:note[count(preceding::*[local-name()=$pagination-element]) = $page_id]">
						<xsl:variable name="note_count"><xsl:value-of select="count(preceding::tei:note) + 1"/></xsl:variable>
						<!--<p><xsl:value-of select="$note_count"/>. <a href="#noteref_{$note_count}" name="note_{$note_count}">[<xsl:value-of select="preceding::tei:cb[1]/@xml:id"/>, l. <xsl:value-of select="preceding::tei:lb[1]/@n"/>]</a><xsl:text> </xsl:text> <xsl:value-of select="."/></p>-->
						<span class="note">
							<span style="position:absolute;left:0.5em"><a href="#noteref_{$note_count}" name="note_{$note_count}"><xsl:value-of select="$note_count"/></a>. </span>
							<xsl:apply-templates mode="#current"/>
						</span><br/>                                                                
					</xsl:for-each></span><xsl:text>&#xa;</xsl:text>                                                                
				
			</xsl:if>
			
			
		</body>
	</xsl:template>
	
	
                <xsl:template match="*">
                                <xsl:choose>
                                	<xsl:when test="descendant::tei:p|descendant::tei:ab">
                                		<div>
                                			<xsl:call-template name="addClass"/>
                                			<xsl:apply-templates/></div>
                                		<xsl:text>&#xa;</xsl:text>
                                	</xsl:when>
                                	<xsl:otherwise><span>
                                		<xsl:call-template name="addClass"/>
                                		<xsl:if test="self::tei:add[@del]">
                                			<xsl:attribute name="title"><xsl:value-of select="@del"/></xsl:attribute>
                                		</xsl:if>
                                		<xsl:apply-templates/></span>
                                	<xsl:call-template name="spacing"/>
                                	</xsl:otherwise>
                                </xsl:choose>
                </xsl:template>
                
                <xsl:template match="@*|processing-instruction()|comment()">
                                <!--<xsl:copy/>-->
                </xsl:template>
                
<!--                <xsl:template match="comment()">
                                <xsl:copy/>
                </xsl:template>
-->                
                <xsl:template match="text()">
                                <xsl:value-of select="normalize-space(.)"/>
                </xsl:template>
                
                <xsl:template name="addClass">
                	<xsl:attribute name="class">
                		<xsl:value-of select="local-name(.)"/>
                		<xsl:if test="@type"><xsl:value-of select="concat('-',@type)"/></xsl:if>
                		<xsl:if test="@subtype"><xsl:value-of select="concat('-',@subtype)"/></xsl:if>
                		<xsl:if test="@rend"><xsl:value-of select="concat('-',@rend)"/></xsl:if>
                	</xsl:attribute>                	
                </xsl:template>
                
                <xsl:template match="tei:p|tei:ab|tei:lg">
                	<p>
                		<xsl:call-template name="addClass"/>
                		<xsl:apply-templates/>
                	</p>
                	<xsl:text>&#xa;</xsl:text>
                </xsl:template>
	
	<xsl:template match="tei:head">
		<h2>
			<xsl:call-template name="addClass"/>
			<xsl:apply-templates/>
		</h2>
	</xsl:template>
	
	<xsl:template match="tei:gap">
		<span class="gap">
			<xsl:if test="@quantity and @unit">
				<xsl:attribute name="title"><xsl:value-of select="concat(@quantity,' ',@unit)"/></xsl:attribute>
			</xsl:if>
			<xsl:text>[...]</xsl:text>
		</span>
		<xsl:call-template name="spacing"/>
	</xsl:template>
                
	<xsl:template match="//tei:lb">
		<xsl:variable name="lbcount">
			<xsl:choose>
				<xsl:when test="ancestor::tei:ab"><xsl:number from="tei:ab" level="any"/></xsl:when>
				<xsl:when test="ancestor::tei:p"><xsl:number from="tei:p" level="any"/></xsl:when>
				<xsl:otherwise>999</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="@rend='hyphen(-)'"><span class="hyphen">-</span></xsl:if>
		<xsl:if test="@rend='hyphen(=)'"><span class="hyphen">=</span></xsl:if>
		<!--<xsl:if test="ancestor::tei:w and not(contains(@rend,'hyphen'))"><span class="hyphen-added">-</span></xsl:if>-->
		<xsl:if test="not($lbcount=1) or preceding-sibling::node()[matches(.,'\S')]"><br/><xsl:text>&#xa;</xsl:text></xsl:if>
		<xsl:if test="@n and not(@rend='prose')">
			<xsl:choose>
				<xsl:when test="matches(@n,'^[0-9]*[05]$')">
					<!--<a title="{@n}" class="verseline" style="position:relative"> </a>-->
					<!--<span class="verseline"><span class="verselinenumber"><xsl:value-of select="@n"/></span></span>-->
					<span class="verselinenumber"><xsl:value-of select="@n"/></span>
					
				</xsl:when>
				<xsl:when test="matches(@n,'[^0-9]')">
					<!--<a title="{@n}" class="verseline" style="position:relative"> </a>-->
					<!--<span class="verseline"><span class="verselinenumber"><xsl:value-of select="@n"/></span></span>-->
					<span class="verselinenumber"><xsl:value-of select="@n"/></span>
				</xsl:when>
				<xsl:otherwise>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	<!-- Page breaks -->                
	<xsl:template match="//*[local-name()=$pagination-element]">
		
		<xsl:variable name="next-word-position" as="xs:integer">
			<xsl:choose>
				<xsl:when test="following::*[local-name()=$word-element]">
					<xsl:value-of select="count(following::*[local-name()=$word-element][1]/preceding::*[local-name()=$word-element])"/>
				</xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="next-pb-position" as="xs:integer">
			<xsl:choose>
				<xsl:when test="following::*[local-name()=$pagination-element]">
					<xsl:value-of select="count(following::*[local-name()=$pagination-element][1]/preceding::*[local-name()=$word-element])"/>
				</xsl:when>
				<xsl:otherwise>999999999</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="next-word-id">
			<xsl:choose>
				<xsl:when test="$next-pb-position - $next-word-position = 999999999">w_0</xsl:when>
				<xsl:when test="$next-pb-position &gt; $next-word-position"><xsl:value-of select="following::*[local-name()=$word-element][1]/@id"/></xsl:when>
				<xsl:otherwise>w_0</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		
		
		<xsl:variable name="editionpagetype">
			<xsl:choose>
				<xsl:when test="ancestor::tei:ab">editionpageverse</xsl:when>
				<xsl:otherwise>editionpage</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="pagenumber">
			<xsl:choose>
				<xsl:when test="@n"><xsl:value-of select="@n"/></xsl:when>
				<xsl:when test="@facs"><xsl:value-of select="substring-before(@facs,'.')"/></xsl:when>
				<xsl:otherwise>[NN]</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		
		<xsl:variable name="page_id"><xsl:value-of select="count(preceding::*[local-name()=$pagination-element])"/></xsl:variable>
		
		<xsl:if test="//tei:note[not(@place='inline') and not(matches(@type,'intern|auto'))][following::*[local-name()=$pagination-element][1][count(preceding::*[local-name()=$pagination-element]) = $page_id]]">
			<xsl:text>&#xa;</xsl:text>
			<br/>
			<br/>			
			<span style="display:block;border-top-style:solid;border-top-width:1px;border-top-color:gray;padding-top:5px">                                                
				<xsl:for-each select="//tei:note[following::*[local-name()=$pagination-element][1][count(preceding::*[local-name()=$pagination-element]) = $page_id]]">
					<xsl:variable name="note_count"><xsl:value-of select="count(preceding::tei:note) + 1"/></xsl:variable>
					<!--<p><xsl:value-of select="$note_count"/>. <a href="#noteref_{$note_count}" name="note_{$note_count}">[<xsl:value-of select="preceding::tei:cb[1]/@xml:id"/>, l. <xsl:value-of select="preceding::tei:lb[1]/@n"/>]</a><xsl:text> </xsl:text> <xsl:value-of select="."/></p>-->
					<span class="note">
						<span style="position:absolute;left:0.5em"><a href="#noteref_{$note_count}" name="note_{$note_count}"><xsl:value-of select="$note_count"/></a>. </span>
						<xsl:apply-templates mode="#current"/>
					</span><br/>                                                                
				</xsl:for-each></span><xsl:text>&#xa;</xsl:text>                                                                
			
		</xsl:if>
		
		
		<xsl:text>&#xa;</xsl:text>
		<br/><xsl:text>&#xa;</xsl:text>
		
			<a class="txm-page" title="{count(preceding::*[local-name()=$pagination-element]) + $page-number-adjust}" next-word-id="{$next-word-id}"/>
		
		<span class="{$editionpagetype}"> &lt;<xsl:value-of select="$pagenumber"/>&gt; </span><br/><xsl:text>&#xa;</xsl:text>
	</xsl:template>
	
	<!-- Notes -->
	<xsl:template match="tei:note">
		<!--<span style="color:violet"> [<b>Note :</b> <xsl:apply-templates/>] </span>-->	
		<xsl:variable name="note_count"><xsl:value-of select="count(preceding::tei:note) + 1"/></xsl:variable>
		<xsl:variable name="note_content">
			<xsl:choose>
				<xsl:when test="descendant::txm:form">
					<xsl:for-each select="descendant::txm:form">						
						<xsl:value-of select="."/>
						<xsl:if test="not(matches(following::txm:form[1],'^[.,\)]')) and not(matches(.,'^\S+[''’]$|^[‘\(]$'))">
							<xsl:text> </xsl:text>
						</xsl:if>
					</xsl:for-each>
				</xsl:when>
				<xsl:otherwise><xsl:value-of select="normalize-space(.)"/></xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="matches(@type,'intern|auto')"></xsl:when>
			<xsl:when test="@place='inline'"><span class="note"> (Note : <xsl:value-of select="$note_content"/>)</span></xsl:when>
			<xsl:when test="not(@place='inline') and not(matches(@type,'intern|auto'))">
				<a title="{$note_content}" style="font-size:75%;position:relative;top:-5px" href="#note_{$note_count}" name="noteref_{$note_count}">[<xsl:value-of select="$note_count"/>]</a>
			</xsl:when>
			<xsl:otherwise><span class="noteref" title="{$note_content}">[•]</span></xsl:otherwise>
		</xsl:choose>
		<xsl:call-template name="spacing"/>                                
	</xsl:template>
	
	<xsl:template match="tei:bibl">
		<span class="noteref" title="{normalize-space(.)}">[•]</span>
	</xsl:template>
	
	<xsl:template match="a[@class='txmpageref']">
		<xsl:copy-of select="."/>
	</xsl:template>
	
	<!--<xsl:template match="tei:note[@place='inline']">
		<span class="noteinline">
			<xsl:apply-templates/>
		</span>
	</xsl:template>
   -->             
                <xsl:template match="//tei:w"><span class="w">
                	<xsl:choose>
                		<xsl:when test="descendant::tei:c//txm:form">
                			<xsl:apply-templates select="descendant::tei:c"/>
                		</xsl:when>
                		<xsl:otherwise>
                			<xsl:if test="@*:id">
                				<xsl:attribute name="id"><xsl:value-of select="@*:id"/></xsl:attribute>
                			</xsl:if>
                			<xsl:attribute name="title">
                				<xsl:for-each select="@*[not(matches(local-name(.),'id'))]">
                					<xsl:value-of select="concat(name(.),' : ',.,' ; ')"/>
                				</xsl:for-each>
                				<xsl:if test="descendant::txm:ana">	
                					<xsl:for-each select="descendant::txm:ana">
                						<xsl:value-of select="concat(substring-after(@type,'#'),' : ',.,' ; ')"/>
                					</xsl:for-each>
                				</xsl:if>
                			</xsl:attribute>
                			<xsl:choose>
                				<xsl:when test="descendant::txm:form">
                					<xsl:apply-templates select="txm:form"/>
                				</xsl:when>
                				<xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
                			</xsl:choose>
                		</xsl:otherwise>
                	</xsl:choose>
                                </span><xsl:call-template name="spacing"/></xsl:template>
                
<!--                <xsl:template match="//txm:form">
                                <xsl:apply-templates/>
                </xsl:template>
-->                
	

	<xsl:template name="spacing">
		<xsl:choose>
			<xsl:when test="$inputtype='xmltxm'">
				<xsl:call-template name="spacing-xmltxm"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="spacing-xmlw"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template name="spacing-xmlw">
		<xsl:choose>
			<xsl:when test="ancestor::tei:w"/>
			<xsl:when test="following::tei:w[1][matches(.,'^\s*[.,)\]]+\s*$')]"/>			
			<xsl:when test="matches(.,'^\s*[(\[‘]+$|\w(''|’)\s*$')"></xsl:when>
			<xsl:when test="position()=last() and (ancestor::tei:choice or ancestor::tei:supplied[not(@rend='multi_s')])"></xsl:when>
			<xsl:when test="following-sibling::*[1][self::tei:note]"></xsl:when>
			<xsl:when test="following::tei:w[1][matches(.,'^\s*[:;!?]+\s*$')]">
				<xsl:text>&#xa0;</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text> </xsl:text>
			</xsl:otherwise>
		</xsl:choose>                
	</xsl:template>

	<xsl:template name="spacing-xmltxm">
		<xsl:choose>
			<xsl:when test="ancestor::tei:w"/>
			<xsl:when test="following::tei:w[1][matches(descendant::txm:form[1],'^[.,)\]]+$')]"/>			
			<xsl:when test="matches(descendant::txm:form[1],'^[(\[‘]+$|\w(''|’)$')"></xsl:when>
			<xsl:when test="position()=last() and (ancestor::tei:choice or ancestor::tei:supplied[not(@rend='multi_s')])"></xsl:when>
			<xsl:when test="following-sibling::*[1][self::tei:note]"></xsl:when>
			<xsl:when test="following::tei:w[1][matches(descendant::txm:form[1],'^[:;!?]+$')]">
				<xsl:text>&#xa0;</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text> </xsl:text>
			</xsl:otherwise>
		</xsl:choose>                
	</xsl:template>

                
</xsl:stylesheet>
