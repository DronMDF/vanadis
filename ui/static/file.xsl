<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/file">
<html>
<head>
	<style>
		td {
			font-family: monospace;
		}
	</style>
</head>
<body>
	<h1><xsl:value-of select="path"/></h1>
	<p/>
	<table>
	<xsl:for-each select="line">
		<tr>
			<td><xsl:value-of select="lineno"/></td>
			<td><pre style="margin: 0">
				<xsl:value-of select="code"/>
			</pre></td>
		</tr>
		<xsl:for-each select="issue">
			<xsl:sort select='position'/>
			<tr>
				<td/>
				<td><div style="text-indent: {position}ch">^
					<xsl:value-of select="text"/>
				</div></td>
			</tr>
		</xsl:for-each>
	</xsl:for-each>
	</table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
