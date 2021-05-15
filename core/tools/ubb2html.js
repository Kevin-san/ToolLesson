function ubb2html(altText){
        var altHTML = altText.replace(/\[img\]((https?|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])\[\/img\]/ig,"<br><img src=$1 style=\"max-width:60%; max-height:60%;\" ><br>");
        altHTML = altHTML.replace(/\[img=\d+,\d+\]((https?|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])\[\/img\]/ig, "<br><img src=$1 style=\"max-width:60%; max-height:60%;\" ><br>")
        
        altHTML = altHTML.replace(/\[color=#([0-9a-fA-F]{6})\]/ig, "<span style=\"color:#$1;\">");
        
        altHTML = altHTML.replace(/\[color=rgb\((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]),\s(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]),\s(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\)\]/ig, "<span style=\"color:rgb($1, $2, $3);\">");
        
        altHTML = altHTML.replace(/\[\/color\]/ig, "</span>");
        
        altHTML = altHTML.replace(/\[b\]/ig, "<strong>");
        
        altHTML = altHTML.replace(/\[\/b\]/ig, "</strong>");
        
        altHTML = altHTML.replace(/\[i\]/ig, "<em>");
        
        altHTML = altHTML.replace(/\[\/i\]/ig, "</em>");
        
        altHTML = altHTML.replace(/\[u\]/ig, "<span style=\"text-decoration: underline\">");
        
        altHTML = altHTML.replace(/\[\/u\]/ig, "</span>");
        
        altHTML = altHTML.replace(/\[font=([0-9a-zA-Z ,&;]+)\]/ig, "<font face=\"$1\">");
        
        altHTML = altHTML.replace(/\[\/font\]/ig, "</font>");
        
        altHTML = altHTML.replace(/\[size=(\d+)px\]/ig, "");
        
        altHTML = altHTML.replace(/\[\/size\]/ig, "");
        
        altHTML = altHTML.replace(/\[align=(left|right|center)\]/ig, "<div style=\"text-align: left\">");
        
        altHTML = altHTML.replace(/\[\/align\]/ig, "</div>");
        
        altHTML = altHTML.replace(/\[url=(.*)](.*)\[\/url\]/ig, "<a href=\"$1\" target=\"_blank\">$2</a>");
        
        altHTML = altHTML.replace(/\[url](.*)\[\/url\]/ig, "<a href=\"$1\" target=\"_blank\">$1</a>");
        
        altHTML = altHTML.replace(/\[email=(.*)](.*)\[\/email\]/ig, "<a href=\"mailto:$1\">$2</a>");
        return altHTML;
}