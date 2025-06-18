import streamlit as st
import os
import time
from streamlit.components.v1 import html
import openai
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from serpapi import GoogleSearch

# OpenAI-API-Key aus Secrets laden (lokal oder online)
openai.api_key = st.secrets["openai"]["api_key"]
serpapi_key = st.secrets["serpapi"]["serpapi_key"]

# Momente
zeitstrahl = [
{"datum": "24.01.2022",
         "titel": "Match",
         "text": "Ich weiß nicht, ob es wirklich genau an diesem Tag war, aber das sind die ersten Nachrichten, die ich von dir gescreenshottet habe. Ich bin so unendlich froh, dass ich zu der Zeit nach recht gewischt habe, um dich treffen zu dürfen. Auch wenn wir diese Story nicht immer als Kennenlerngeschichte erzählen wollen, weil sie nicht ganz so romantisch ist, bin ich trotzdem sehr dankbar, dass ich dich auf diese Weise kennenlernen durfte.",
         "bild": "1_Match.jpg"},
{"datum": "24.01.2022",
         "titel": "Erste Nachrichten",
         "text": "Hier sind unsere ersten Nachrichten. Ich wusste direkt, dass ich mit dir viel Spaß haben werde, weil du dich direkt auf meine etwas verrückte Art eingelassen hast. Ich meine, du hast dich mit mir getroffen, obwohl ich so viel Blödsinn geschrieben habe. Da konntest du dann ja nur ein guter Fang sein. Danach sind wir dann mal auf WhatsApp umgestiegen und ich werde niemals unsere ersten Stickerbattle vergessen. Da wusste ich sofort „Mit ihr muss ich mich treffen, es passt einfach zu gut“. Ich hoffe ich bekomme noch viele weitere Treffen.",
         "bild": "2_Erste_Nachrichten.jpg"},
{"datum": "04.02.2022",
        "titel": "Erster Tag zusammen",
        "text": "Unser erster Tag zusammen. Du hast mich gefragt, ob ich auf den Geburtstag von Malle kommen möchte. Und ich bin bis heute so glücklich darüber, dass ich das einfach gemacht habe. Natürlich war ich sehr nervös, aber dann mit dir ein bisschen zu reden, hat meine Nervosität weggemacht. Und natürlich auch die Sex-on-the-Beach-Bowl. Aber ich glaube auch ohne die hätten wir uns direkt super verstanden.",
        "bild": "3_Erster_Tag_zusammen.jpg"},
{"datum": "04.02.2022",
        "titel": "Erster Kuss",
        "text": "Und dann gab es am gleichen Abend auch unseren ersten Kuss. Und ich finde es im Nachhinein irgendwie so schön, dass das der Anfang war von so vielen schönen Momenten war. Von so vielen schönen Küssen. Und ich bin noch viel froher, dass ich mich an dem Tag dann noch auf die Nase legen musste. Vielleicht hätten wir auch so viel erlebt, wenn ich das nicht gemacht hätte. Aber lieber hab ich mir einmal wehgetan und dadurch diese Zeit mit dir erleben dürfen, als es nicht gemacht zu haben. Und ich würde es immer wieder machen",
        "bild": "3_2_Erster Kuss.jpg"},
{"datum": "18.02.2022",
        "titel": "Erstes Date",
        "text": "Hier habe ich leider nur ein Bild, wie wir das Date abgemacht haben 😅. Aber auch wenn du mir bis heute vorhälst, dass ich an dem Tag nur einen Salat gegessen hab, war es ein sehr schöner Tag mit dir. Ich weiß noch wie wir im windigen Auto saßen, wie du mir von dem Open Water Film erzählt hast und mir gesagt hast, dass du Hai-Dokus cool findest. Und auch wie wir uns zum Abschied geküsst haben. Ich glaube wir waren da beide sehr nervös. Aber auch hier bin ich sehr froh, dass wir es so gemacht haben, wie es am Ende war. Denn so war es perfekt.",
        "bild": "4_Erstes_Date.jpg"},
{"datum": "21.02.2022",
        "titel": "HSM & Camp Rock",
        "text": "Unser erstes Treffen bei mir. Und extra alles für dich bereitgestellt, was du gerne magst (und noch andere Sachen). Auch wenn ich dich gegen deinen Willen durch 5 Musical-Filme gequält habe (Es tut mir immer noch sehr leid. Du hättest was sagen können) fand ich den Abend und natürlich auch die Nacht sehr schön mit dir. Das erste Mal, dass wir zusammen übernachtet haben und ich habe mich danach auf mehrere solcher Tage und Abende gefreut. Bis heute fand und finde ich es immer noch schön, wenn ich weiß, dass du neben mir schläfst.",
        "bild": "4_2_HSM.jpg"},
{"datum": "22.03.2022",
        "titel": "Pullover",
        "text": "Danach ging es für dich leider recht schnell nach Münster. Wir hatten uns natürlich noch ein paar Mal gesehen, aber New York stand ja auch vor der Tür. Als ich dann nach Münster gekommen, hatte ich nicht nur ein paar Nahtoderfahrungen auf dem Send (Kettenkarussel, dieses Partyding, dein Döner👀) sondern auch eine sehr schöne Zeit mit dir. Eine die ich einfach nicht verlieren wollte. Und damit du mich nicht vergisst, habe ich dir einen Pullover von mir mitgegeben. Und ich hoffe, dass du dich gefreut hast. Ich wünsche mir so sehr dir noch öfter was kleines schenken zu können.",
        "bild": "5_Pullover.jpg"},
{"datum": "09.04.2022",
         "titel": "R-Herz",
         "text": "Als du dann in New York warst, haben wir täglich (für mich) bis in die späte Nacht geschrieben. Und auch wenn es für dich nicht immer leicht war, hoffe ich, dass du es bis heute immer noch nicht bereut hast. Mir hat das immer sehr viel bedeutet. Und als ich dir dann helfen konnte bei ein paar Programmiersachen (auch wenn ich selber keine Ahnung hatte), dachte ich, dass ich dir so eine kleine Freude machen kann. Auch wenn ich es aus dem Internet geklaut habe. Aber ich hoffe, dass ich dir das irgendwann wirklich mal machen kann, wenn ich ein bisschen besser in dem allen bin.",
         "bild": "6_R_Herz.jpg"},
{"datum": "15.04.2022",
         "titel": "Discord",
         "text": "Dann habe ich dich dazu gebracht dir Discord runterzuladen. Ganz nach dem TikTok-Motto „Und dann hab ich mir für diesen Typen auch noch Discord runtergeladen, was ist denn los mit mir?“. Aber diese Zeit mit dir, einfach mit dir zu sprechen und bei deiner täglichen Skin-Routine oder bei deinem Kochen dabei gewesen zu sein, ist bis heute so eine schöne Erinnerung. Oder als wir ein paar Spiele wie Make it Meme oder Geoguesser gespielt haben. Jedes Mal wenn ich jetzt Make-it-Meme mit den anderen spiele, denke ich irgendwie immer nur daran, wie schön es dann immer war, dass du dabei warst.",
         "bild": "7_Discord.jpg"},
{"datum": "07.07.2022",
         "titel": "Erstes Konzert",
         "text": "Und natürlich hatten wir noch weitere Gespräche als du in New York warst. Dann warst du aber wieder zurück in Deutschland. Ich wäre sehr gerne zu deiner Welcome-Back-Party gekommen, aber leider musste ich ja Corona haben (Das hat sich so bei uns durchgezogen). Als du dann wieder bei mir warst, und das finde ich von mir bis heute immer noch einfach blöd, habe ich dir dann nicht die Wertschätzung direkt gegeben, die du verdient hattest. Etwas, was ich mir nie verzeihen kann. Und es wird mir für immer leid tun. Als erste Aktivität sind wir dann auf das Ed Sheeran Konzert spontan gefahren. Unser erstes Konzert zusammen. Was glaubst du, wie sehr ich hoffe, dass wir im September da wieder gemeinsam hingehen können. Und das verspreche ich dir: Ich werde dich für immer so wertschätzen, wie du es verdient hast.",
         "bild": "8_Erstes_Konzert.jpg"},
{"datum": "15.07.2022",
         "titel": "Emily & Me",
         "text": "Du bist dann häufiger bei mir gewesen (Danke, dass du immer den Weg auf dich genommen hast, bis heute). Ich hatte sogar noch auf der anderen Seite geschlafen, wie es aussieht. Das ist aber das erste Bild von dir, welches du von mir und Emily gemacht hast. Ein Bild, was in den nächsten Monaten und Jahren häufiger aufgekommen ist. Und ich wünsche mir sehr, dass diese Bilder von dir noch öfter in der Zukunft gemacht werden",
         "bild": "9_Emily_Me.jpg"},
{"datum": "24.07.2022",
         "titel": "Gang",
         "text": "An diesem Tag haben wir zum ersten Mal etwas zu viert gemacht. Es ist so eine schöne Gruppe mit uns vieren, wo wir einfach immer Spaß haben können und irgendwas machen. Die beiden haben dich auch sehr ins Herz geschlossen und sehen dich als eine sehr gute Freundin an. Hoffentlich können wir noch viele weitere Tage zu viert verbringen.",
         "bild": "10_Erste_Mal_Gang.jpg"},
{"datum": "18.08.2022",
         "titel": "Mallorca Herz",
         "text": "Dieses Bild ist bis heute noch witzig. Und ich denke sehr gerne an diesen Tag zurück. Wir beide in Andratx unterwegs und wurden dann von dem anderen Paar gefragt, ob wir nicht auch ein Bild in diesem Herz machen wollen. Wir beide noch so ein bisschen verwirrt, was das genau alles werden soll, aber ich bin sehr froh, dass wir dieses Bild haben. Dieser Urlaub mit dir war wirklich einfach schön.",
         "bild": "11_Mallorca_Herz.jpg"},
{"datum": "19.08.2022",
         "titel": "Mallorca zusammen auf der MA-10",
         "text": "Hier ist noch ein Bild von unserer Rundreise die MA-10 entlang. Diesen Weg da lang zu fahren und unterschiedliche Spots und Bilder zu finden, war wirklich eine der schönsten Sachen die wir auf Mallorca bis jetzt gemacht haben. Es war so schön zusammen die Sachen anzuschauen, auf diesen komischen Turm zu klettern oder zusammen ein paar Bilder zu machen. Danke, dass ich das mit dir machen durfte. Ich werde es niemals vergessen.",
         "bild": "12_Mallorca_zusammen_2022.jpg"},
{"datum": "21.08.2022",
         "titel": "T-Shirt",
         "text": "Leider musste ich dann schon etwas früher abreisen. Ich kann mich noch an den Moment erinnern, als ich alleine durch diese Sicherheitstore gegangen bin. Ich hatte einfach Tränen in den Augen, weil ich dich verlassen musste. Ich war so traurig, dass ich wieder nach Hause musste und ein paar Tage ohne dich war. Das war so ein Erlebnis, wo ich wusste „Ja, das hier ist richtig. Sie ist die richtige Wahl“. Und wenn ich das hier jetzt so schreibe, weiß ich gar nicht, ob ich dir das je erzählt habe. Und dann weiß ich wieder nicht warum ich es nie gesagt habe. Och man..",
         "bild": "13_T-Shirt.jpg"},
{"datum": "02.09.2022",
         "titel": "Zusammenkommen",
         "text": "Ich auf einem Pferd. Das hattest du dir zu der Zeit glaube ich auch anders vorgestellt. Aber es wurde der Tag bevor wir endlich zusammen waren. Und ich werde den 03.09.22 niemals vergessen. Es ist für mich so ein bedeutsames Datum. Es ist einfach unser Datum. Wir beide, zusammen. Dadurch haben wir es offiziell gemacht. Dass wir ein Team sein wollen, dass wir einander so gerne haben, dass wir mit der Person so viel Zeit verbringen wollen, wie es nur geht. Auch wenn wir es erst ein bisschen später gesagt haben: Es hat auch gezeigt, dass wir die Zeit zusammen lieben und die Person gegenüber auch. Ich werden diesen Tag niemals vergessen. Ich hoffe du auch nicht.",
         "bild": "14_Zusammenkommen.jpg"},
{"datum": "09.09.2022",
         "titel": "Erste Hochzeit",
         "text": "Unsere erste Hochzeit. Und es war direkt die deines Vaters. Für mich natürlich eine große Ehre, dass du mich dazu direkt mitnehmen wolltest, auch wenn wir erst in den Startlöchern waren. Und auch, wenn es für dich natürlich eine Achterbahn der Gefühle war (mehr bergab als bergauf) war es trotzdem ein schöner Tag zu zweit. Wir konnten viel Lachen (siehe Bild), wir konnten uns dabei auch ein bisschen besser kennenlernen und ein paar schöne Fotos machen. Auch wenn ich finde, dass wir uns doch noch mal ein Stück weiterentwickelt haben (Wie sehe ich denn aus???).",
         "bild": "15_Erste_Hochzeit.jpg"},
{"datum": "06.10.2022",
         "titel": "Erste Boston-Bar Party",
         "text": "Unsere erste Party in der Boston Bar. Und irgendwie auch meine erste Uni-Party. Ich kannte das sonst ja gar nicht. Auch wenn ich am Ende nicht der größte Fan der Boston Bar bin (kann ja noch werden), fand ich den Abend sehr schön. Und dann ist dieses Bild entstanden. Irgendwie auch das erste Kühlschrankbild von uns. Auch wenn wir ein bisschen, wie Bronzestatuen aussehen, ist es trotzdem immer wieder ein schöner Moment, wenn ich dieses Bild sehe. Ich wünsche mir noch ganz viele Bilder von dieser Sorte mit dir.",
         "bild": "16_Erste_Boston_Bar.jpg"},
{"datum": "09.10.2022",
         "titel": "Erste Mal bei Oma & Opa",
         "text": "Hier sind wir das erste Mal gemeinsam bei deinen Großeltern gewesen. Ich weiß gar nicht mehr, was es genau war. Der Geburtstag von deiner Oma? Aber auch hier fand ich es wieder schön dabei gewesen zu sein. Auch wenn ich natürlich nicht der größte Fan von Hemden bin (ich versuche da wirklich dran zu arbeiten) sehen wir doch echt gut auf dem Bild aus (außer meine Schuhe. Das war nix). Die weiteren Feste mit deiner Familie waren dann auch immer schön. Aber da das das erste war, wird es mir immer am besten in Erinnerung bleiben.",
         "bild": "17_2_erste_Mal_bei_Familie.jpg"},
{"datum": "09.10.2022",
         "titel": "Maislabyrinth",
         "text": "Danach ging es dann noch ins Maislabyrinth. Auch wenn wir nicht wirklich den designierten Weg gegangen sind, war es trotzdem eine sehr lustige Erfahrung. Vor allem auch, als wir versucht haben den Mais durch die Löcher zu werfen. Ich würde sehr gerne nochmal im Sommer dahin, damit es auch ein bisschen grüner um uns rum ist. Und vielleicht würden wir es dann zusammen richtig schaffen durch das Labyrinth zu kommen.",
         "bild": "17_Mais-Labyrinth.jpg"},
{"datum": "10.12.2022",
         "titel": "I Love YOU",
         "text": "Die Hochzeit von Fabian. Unsere zweite Hochzeit innerhalb von drei Monaten. Das hatten wir uns auch ein bisschen anders vorgestellt. Aber diese Hochzeit wird mir immer in Erinnerung bleiben. Nicht, weil sie so schön war oder da irgendwas tolles passiert ist, sondern wegen dem, was danach passiert ist. Wir beide zusammen auf der Couch und ich hab endlich mal das gesagt, was ich dir die ganze Zeit schon hätte sagen sollen. Und was ich dir am liebsten jeden Tag bis zum Ende meines Lebens sagen würde: ICH LIEBE DICH. Und daran wird sich nie was ändern.",
         "bild": "18_I_Love_YOU.jpg"},
{"datum": "31.12.2022",
         "titel": "Erstes Silvester",
         "text": "Leider habe ich keine Bilder von unserem ersten Weihnachten zusammen. Ich hätte sie sehr gerne gehabt. Wenn du da noch welche haben solltest, würde ich mich über die Bilder freuen. Dann kann ich den Punkt noch ergänzen. Aber unser erstes Silvester. Ich fand es so schön, dass du dich dazu bereit erklärt hast bei unserem Silvester mitzumachen. Das ist nicht selbstverständlich. Sowohl im ersten Jahr, als auch in den anderen beiden Jahren. Also noch einmal danke, dass du immer dabei warst, damit ich mein neues Jahr immer mit meiner Lieblingsperson verbringen konnte. Hoffentlich werden es noch einige mehr. Muss auch nicht immer in dieser Konstellation sein, wir können auch gerne dann woanders hin.",
         "bild": "19_Erstes_Silvester.jpg"},
{"datum": "28.01.2023",
         "titel": "Erster Handyhintergrund",
         "text": "Ich weiß leider nicht, wann genau wir dieses Bild gemacht haben: Aber es ist einfach bis heute ein sehr schönes Bild von uns. Ich schaue es immer noch täglich auf meinem Schreibtisch an und egal wie oft ich draufgucke, bin ich immer wieder glücklich diese ganzen Momente mit dir gemeinsam erlebt zu haben. Es war auch mein erster Handyhintergrund von uns beiden. Zum einen hätte ich das wesentlich früher machen müssen, aber zum anderen bin ich trotzdem einfach froh, dass ich dieses Bild immer so in Erinnerung haben kann. Es wird immer etwas sehr besonderes für mich sein.",
         "bild": "20_Erster_Hintergrund.jpg"},
{"datum": "04.02.2023",
         "titel": "Skifahren",
         "text": "Dann ging es für uns vier in den Skiurlaub. Mein erster wirklicher Skiurlaub und ich bin so froh, dass ich den mit dir zusammen verbringen konnte. Es war wirklich sehr schön, mit dir durch die Gegend zu fahren, irgendwann immer die rote Piste runterzudüsen und zu schauen, wer sich besser schlägt. Ich hoffe so sehr, dass wir das nochmal gemeinsam machen können. Dann ist mein Knie wieder gut und wir können ganz oft durch die Gegend fahren. Ich wünsche mir es einfach so sehr mit dir nochmal Pisten runterzufahren.",
         "bild": "21_Skifahren(1).jpg"},
{"datum": "08.02.2023",
         "titel": "Mehr Skifahren",
         "text": "Dieses Bild von uns ist auch immer ein Favorit von mir gewesen. Irgendwie ist es so schön. Vielleicht, weil ich mal ein bisschen größer bin? 😂 Aber trotzdem denke ich immer wieder sehr gerne an diese Tage und den ganzen Urlaub zurück. Für mich war das eine wunderschöne Erfahrung und etwas, was ich nie vergessen werde. Mit dir diese Erlebnisse gehabt zu haben, werde ich für immer in meinem Herzen behalten.",
         "bild": "22_Skifahren(2).jpg"},
{"datum": "09.02.2023",
         "titel": "Cosmopolitan",
         "text": "Das Bild musste ich einfach mit reinnehmen. Ich finde es immer wieder so lustig. Und ich finde, dass dieses Bild uns so gut beschreibt. Wir haben in dem Moment einfach nicht nachgedacht, sondern wollten nur etwas Lustiges zusammen machen. Und das zeigt so gut, wie lustig wir zusammen sein können und wie viel Spaß wir zusammen haben können. Auch wenn ich nie wieder einen Cosmopolitan trinken möchte, werde ich trotzdem bei dem Namen immer an diesen Moment denken und egal in welcher Situation schmunzeln müssen",
         "bild": "23_Cosmopolitan.jpg"},
{"datum": "16.02.2023",
         "titel": "Erstes Karneval",
         "text": "Unser erstes Karneval. Ja. Wo fange ich da an? Zum einen so schön, dass du den Tag oder die Tage so angenommen hast, obwohl du das gar nicht so mochtest bzw. kanntest. Zum anderen natürlich einfach nur blöd von mir und ich werde mich für immer für diese Tage entschuldigen. Aber ich hoffe, dass ich dir durch die letzten Jahre gezeigt habe, dass das nicht mehr die Person ist, die ich jetzt bin. Dass du mir so viel wichtiger bist, als alles andere und auch jede andere Person auf der Welt. Und ich hoffe so sehr, dass ich dir das in den nächsten Karnevals weiterhin zeigen kann.",
         "bild": "24_Erstes_Karneval.jpg"},
{"datum": "28.04.2023",
         "titel": "Macklemore",
         "text": "Aber zum Glück hast du mir doch irgendwie verziehen. Auch wenn ich weiß, dass du es nie vergessen hast, hast du immer dein bestes gegeben daran zu glauben, dass ich in der Zukunft nicht so sein werde. Und ich hoffe, dass ich dieses Vertrauen auch bestätigen konnte. Da du mir aber verziehen hast, konnte wir weitere Sachen erleben. Beispielsweise sind wir als unglaublich angsteinflößende Gang durch Köln gelaufen (siehe Bild), um zum Macklemore-Konzert zu gehen. Das war schon cool und ich glaube bis heute immer noch das coolste Konzert, dass wir bis jetzt gesehen haben.",
         "bild": "25_Macklemore.jpg"},
{"datum": "13.05.2023",
         "titel": "Japan-Tag",
         "text": "Der Japan-Tag. Als Tag irgendwie ein Reinfall. Aber man muss sagen, wir waren auch noch nicht so im Sushi/Ramen Game. Vielleicht wäre der Japan Tag heutzutage etwas cooler. Aber nichtsdestotrotz fand ich den Tag mit dir einfach schön. Dieses Bild von uns ist toll, der Tag selber war eigentlich schön (er war nur nicht anders, weil Japan-Tag war) und am Ende das Feuerwerk zusammen zu schauen war auch schön. Mit allem, was wir so japanisches gegessen haben mittlerweile, würde ich den Japan-Tag mit dir gerne nochmal machen. Vielleicht isses diesmal was für uns. Also solange wir uns nicht als Anime-Charaktere verkleiden müssen",
         "bild": "26_Japan_Tag.jpg"},
{"datum": "22.05.2023",
         "titel": "Pool bauen",
         "text": "Im Sommer 2023 startete dann auch das Projekt Pool. Und du hast fleißig deine Bachelorarbeit geschrieben. Und nicht nur geschrieben, sondern komplett abgerissen mit deiner 1,0. Ich fand es einfach so schön, dass du die ganze Zeit dabei warst. Und irgendwie hätten mir auch die kleinen Kommentare nebenbei bei dem Bau gefehlt. Keine Ahnung, egal bei was und egal wie. Du machst alles für mich so viel besser. Egal ob Arbeit, bauen oder das Leben generell. Du bist einfach immer mein Lichtblick. Danke, dass du immer für mich da warst.",
         "bild": "27_Pool_bauen.jpg"},
{"datum": "25.05.2023",
         "titel": "Hippo oder Gänseblümchen?",
         "text": "Ich kann mich an den Tag hier irgendwie noch gut erinnern. Wir wollten nachdem ich von der Arbeit kam ins Gym gehen und ihr beide habt in dem Park auf mich gewartet. Und irgendwie sind wir dann einfach ein bisschen länger noch da geblieben. Es war super Wetter, wir haben gequatscht und dann diese witzigen Bilder gemacht. Ich weiß noch dein Meme, was du davon erstellt hast, als du meintest, dass du die Blume immer anschaust wie ein Hippo. Man, ich wünsche mir so sehr dir nochmal Hippos mitbringen zu können. Einfach nur, damit ich nochmal sehen kann, wie komisch du die kleinen Dinger isst. Ich vermisse das",
         "bild": "28_Hippo-Park.jpg"},
{"datum": "26.05.2023",
         "titel": "Stockbrot im Garten",
         "text": "Hier waren wir das erste Mal im Garten von Christoph und haben ganz entspannt den Abend mit den beiden und Josy und Jonas verbracht. Irgendwie kommt es mir noch gar nicht so lange her vor, aber es sind doch schon zwei Jahre. Der Tag war aber auch wieder schön, vor allem, als wir dann am Ende an dem Lagerfeuer saßen und Stockbrot gemacht haben. Du hast deins gefühlt direkt verbrannt und meins hat ewig gedauert. Ich dachte wirklich ich bin Stockbrot-Experte in der Zeit und dass meins einfach super wird. Ja, ne, war am Ende noch roh und hat viel zu lange gebraucht 😂",
         "bild": "30_Stockbrot_Garten.jpg"},
{"datum": "04.06.2023",
         "titel": "Mini-Golf",
         "text": "Ein bisschen Mini-Golf? Irgendwann haben wir uns dann im Mini-Golf gemessen. Die Revanche für den einen Nachmittag in Balken. Aber ich weiß gar nicht mehr, ob ich an dem Tag gewonnen habe. Aber es ist egal. Im Nachhinein habe ich an jedem Tag mit dir gewonnen. Weil ich ihn mit dir verbringen konnte. Und nach dem Mini-Golf wurde es ja sogar noch schöner. Okay, die Wacht am Rhein war nix, aber als wir dann langsam nach unten gegangen sind, war es einfach so ein toller Tag.",
         "bild": "31_Mini-Golf.jpg"},
{"datum": "04.06.2023",
         "titel": "Fotoshooting am Rhein",
         "text": "Denn wir haben die schönsten Fotos gemacht. Immer wieder wenn ich dieses Bild sehe, denke ich, das könnte auch aus irgendeiner Kampagne sein. Wie dein Rock da liegt, wie wir aussehen, wie einfach alles da ist. Ich denke so gerne daran zurück. Wie du deine Bilder mit der Uhr versucht hast zu machen, wie wir das Handy ausrichten mussten und auch wie witzig die Begegnung am Ende mit der älteren Frau war, die oben noch ein Bild von uns machen wollte. Ich hab das während dem Bilder raussuchen nochmal gefunden. Es ist echt nix geworden 😂 Aber das ist ja nicht schlimm. Die Bilder in meinem Kopf für diesen Tag werden immer da sein. Und ich hoffe, dass ich so einen Tag nochmal mit dir haben kann. Das wünsche ich mir wirklich sehr",
         "bild": "32_Foto-Shooting.jpg"},
{"datum": "22.06.2023",
         "titel": "Nizza Salat",
         "text": "Das erste Mal zusammen im Krankenhaus. Und es war nicht ich? Hätte uns das jemand nach unserem ersten Date gesagt, hätten wir es vermutlich nicht geglaubt. Aber leider fiel das Billardspielen relativ schnell ins Wasser, da der Nizza-Salat nicht ganz so gut für dich war. Das war auch meine erste Begegnung mit einer allergischen Reaktion von dir. Ich hatte schon auch Angst um dich, weil ich nicht genau wusste, wie schlecht es dir dann gehen wird. Zum Glück hat sich das ja recht schnell wieder eingekriegt, aber es war trotzdem ein bisschen eine komische Erfahrung. Aber das ist ja egal. Ich wäre bei jeder einzelnen Sache für die du irgendwo hinmusst immer für dich da und würde immer an deiner Seite sein, bis es endlich wieder besser wird.",
         "bild": "33_Nizza-Salat.jpg"},
{"datum": "28.06.2023",
         "titel": "Captain Unterhose",
         "text": "Dazu muss ich glaube ich gar nicht viel sagen 😂 Das zeigt einfach, wie du bist. Du bist die lustigste Person die ich kenne. Du bringst mich immer zum Lachen, egal ob du es versuchst oder nicht. Und ich hoffe so sehr, dass ich noch ganz oft über deine Sachen lachen darf. Ich hoffe, dass ich das mein ganzes Leben machen darf. Damit machst du einfach jeden Tag von mir so viel besser.",
         "bild": "34_Captain_Unterhose.jpg"},
{"datum": "16.07.2023",
         "titel": "Sommer 2023 einläuten",
         "text": "Der Pool war glaube ich endlich fertig, aber das Wetter war noch nicht ganz sooo super. Also saßen wir nur ein bisschen draußen rum und auch hier hattest du wieder eine lustige Idee. Findest du mir stehen die Locken? Ich finde schon. Wenn ich dieses Bild schon wieder sehe, vermisse ich so sehr, dass du deinen Kopf so auf mich legst. Wenn das nochmal passieren würde, wäre ich glaube ich die glücklichste Person auf der Welt.",
         "bild": "35_Sommer_23.jpg"},
{"datum": "28.07.2023",
         "titel": "Top-Golf",
         "text": "Wir das erste Mal bei Topgolf. Das erste Mal überhaupt einen Golfschläger in der Hand, anstelle einer Wii- oder Switch-Fernbedienung (Mini-Golf zählt nicht). Und wir waren alle.. echt kacke 😂 Aber, dass du am Ende dein Talent in Angry Birds gefunden hast, war schon nicht schlecht. Du hast uns da wirklich alle abgezogen. Und an dem Tag war dein Outfit auch echt super schön. Du warst auf jeden Fall die stylishste auf dem ganzen Golffeld (oder wie man das da nennt). Das zweite Mal war schon was besser, aber ich hoffe sehr darauf, dass wir sowas noch öfter machen können. Mit dir macht mir sowas immer am meisten Spaß.",
         "bild": "36_Topgolf_1.jpg"},
{"datum": "05.08.2023",
         "titel": "Brumm-Flitzer",
         "text": "Ja, wen haben wir denn da? Brumm-Flitzer!! Auch wenn er irgendwie nur als Übergang gedacht war, habe ich ihn wirklich ins Herz geschlossen. Jedes Mal wenn ich so einen Mini sehe, muss ich direkt an dich denken, direkt an Brumm-Flitzer und an dein Gesicht, als du das erste Mal mit ihm angedüst kamst. Wie happy du einfach warst, dass du mit ihm durch die Gegend fahren konntest und natürlich auch, dass du nicht mehr so oft Bahn fahren musstest. Jeden Tag, den ich dann nach Hause kam und Brumm-Flitzer auf der Straße gesehen habe, war ich so unglaublich froh nach Hause zu kommen. Weil ich wusste, dass du da bist. Und dadurch war alles so viel schöner. Was ich nicht alles dafür geben würde, um noch einmal nach Hause zu kommen und Brumm-Flitzer auf der Straße zu sehen. Einfach nur, um zu wissen, dass du auf mich wartest.",
         "bild": "37_Brummflitzer.jpg"},
{"datum": "15.08.2023",
         "titel": "Mallorca 2023",
         "text": "Wir beide wieder auf Mallorca. Immer das größte Highlight meines Jahres, weil ich dann mit dir endlich so viel Zeit verbringen konnte. Sonst hatten wir immer irgendwas, wo wir uns paar Tage nicht gesehen haben, aber auf Mallorca sind wir immer zusammen und immer ein Team. Es ist immer so schön mit dir durch die Insel zu fahren, im Pool zu sein, zusammen ein bisschen zu wohnen, auch wenn es auf einer anderen Ebene ist. Aber dieser Urlaub 2023 ist glaube ich bis jetzt der schönste Urlaub, den ich je hatte. Wir beide zusammen. Wir hatten Spaß, haben komische Videos gemacht und waren einfach zusammen wir beide. Ich wünsche mir manchmal so sehr, dass ich das nochmal erleben kann.",
         "bild": "38_Mallorca_23.jpg"},
{"datum": "17.08.2023",
         "titel": "P",
         "text": "Es war nur so eine kleine Spielerei. Aber als du dieses Herz mit dem P auf den Pool gemalt hast, war ich einfach glücklich. Diese kleinen Dinge, die einfach zeigen, dass die Liebe echt ist. Etwas wo man nicht drüber nachdenkt, wie der andere es aufnimmt, sondern man einfach macht, weil es sich richtig anfühlt. Es ist so schön und ich bin so froh, dass wir davon ein Bild gemacht haben, sodass ich es immer wieder anschauen kann. Was würde ich alles für diesen Moment nochmal geben..",
         "bild": "39_P.jpg"},
{"datum": "20.08.2023",
         "titel": "Speedboot-Tour",
         "text": "Unsere „Speedboot“-Tour 😂. Na gut, schnell war sie nicht. Aber es war trotzdem sehr schön, dass wir ein bisschen übers Wasser gedüst sind. Einfach zusammen ein bisschen über die Wellen zu gleiten. Und dieses Bild, wo du dich an mich rankuschelst, während wir wieder zurückgefahren sind. Sowas ist so unglaublich toll. Wir beide, zusammen mit einer kalten Coli und einer schönen Aktivität. Ich glaube nichts auf der Welt kann solche Momente für mich toppen.",
         "bild": "40_Bootstour.jpg"},
{"datum": "20.08.2023",
         "titel": "Love in Pool",
         "text": "Diese Bilder waren auch so schön irgendwie. Wir beide im Pool, zuerst versucht ein paar gestellte Bilder zu machen, aber am Ende waren sie einfach echt. In dem Bild hier, wo wir beide uns einfach nur anschauen. Das war nicht gestellt, weil wir das auch oft genug ohne Kamera gemacht haben. Keine Ahnung, für mich zeigt es, dass es zwischen uns immer echt war. Wir uns immer geliebt haben, egal ob für ein Foto oder einfach nur so.",
         "bild": "41_Love_in_Pool.jpg"},
{"datum": "25.08.2023",
         "titel": "Formentor",
         "text": "Dann der kleine Ausflug nach Formentor. Zum Glück sind wir da dann noch reingekommen, ist ja scheinbar nicht selbstverständlich. Aber auch das war so ein schöner Tag. Auch wenn ich immer ein bisschen Angst um unsere Sachen hatte, die irgendwo weit weg lagen 😂. Aber am Ende ist ja alles gut gegangen. Und die Fotos die wir dann mit diesem Wasserdingsi fürs Handy gemacht haben, waren dann auch einfach schön. Ich freue mich jedes Mal, wenn die mir angezeigt werden.",
         "bild": "42_Strand.jpg"},
{"datum": "26.08.2023",
         "titel": "Love under water",
         "text": "Hier haben wir dann dieses Wasserdingsi so ganz ausgenutzt. Ein paar Knutschfotos unter Wasser. Und ich finde, sie sind super geworden. Und auch hier ist es einfach wieder nicht gestellt. Klar, sind wir mit der Intention unter Wasser gegangen, aber ich weiß nicht, es wirkt für mich so echt. Ich weiß nicht, ob du verstehst, was ich meine. Es sieht einfach so richtig aus. Und ich würde wirklich alles dafür eintauschen, um mit dir nochmal in diesem Pool zu sein, nochmal so einen Urlaub zu haben und nochmal solche Bilder machen zu können.",
         "bild": "43_Love_under_water.jpg"},
{"datum": "24.09.2023",
         "titel": "Mahiki",
         "text": "Back in Germany. Und wo feiert es sich am besten? In der Location von Love is blind 👀. Das wussten wir zu der Zeit aber noch nicht. Wir zusammen im Mahiki (?). Heißt das so? Es war auf jeden Fall besser als in der Boston Bar und ich würde wirklich gerne nochmal mit dir in diese ganzen Läden gehen. Ich vermisse es mit dir zu feiern und zu sehen, wie viel Spaß es dir macht mit deinen Freunden und mir einfach rumzutanzen.",
         "bild": "44_Mahiki.jpg"},
{"datum": "28.09.2023",
         "titel": "Microsoft-Support",
         "text": "Hier ist wieder so ein Beispiel, was für komische Sachen wir gemacht haben 😂. Dann ist es auch irgendwie kein Wunder, dass mein Headset am Ende kaputt war. Aber so ein Bild von uns beiden bringt mich wieder zu so vielen Momenten zurück, wo du mich so hart zum Lachen gebracht hast. Du glaubst nicht, wie sehr ich mich danach sehne, dich nochmal Lachen zu hören oder nochmal von dir zum Lachen gebracht zu werden. Das werden immer die schönsten Erinnerungen bleiben.",
         "bild": "45_Calls.jpg"},
{"datum": "07.10.2023",
         "titel": "Graduation",
         "text": "Graduation! Und ich war so stolz auf dich. Wie gut du deinen Abschluss gemacht hast, obwohl auch nicht immer alles einfach war. Wie super deine Abschlussarbeit war, obwohl du die mitten im Sommer auf der Terrasse geschrieben hast. Auch bei dem ganzen Event dabei gewesen zu sein, war so unglaublich schön. Ob es der Tag insgesamt war oder die Feier. Es war alles so toll mit dir zusammen. Ich wäre so gerne dabei, wenn du deinen Master schaffst..",
         "bild": "46_Graduation.jpg"},
{"datum": "07.10.2023",
         "titel": "Graduation Pics",
         "text": "Und die Bilder die wir dann vor dem Essen gemacht haben, waren auch sehr schön. Ich bin bis heute sehr froh, dass dieses Bild auf meinem Nachttisch steht, damit ich immer wieder sehen kann, wie schön wir da zusammen aussehen. Es erinnert mich jedes Mal wieder an diese schönen Zeiten von uns beiden zurück.",
         "bild": "46_2_Graduation(2).jpg"},
{"datum": "14.10.2023",
         "titel": "Kürbis schnitzen",
         "text": "Diese Kürbis-Schnitz-Aktion war auch so witzig. Ich hatte das vorher noch nie gemacht und es war echt sehr lustig das zu machen. Auch wenn er am Ende ein bisschen gruselig war, als er dann zusammengefallen ist. Aber diese Bilder und dieser Tag, wo wir dann diesen kleinen Kürbis geschnitzt haben. Es war toll und ich wünsche mir sehr, das nochmal mit dir machen zu können. Am liebsten jedes Jahr.",
         "bild": "47_Halloween.jpg"},
{"datum": "21.10.2023",
         "titel": "Roly",
         "text": "Roly, Roly, Roly 😂 Dein wohlverdientes Bachelor-Geschenk. Du hast so lange darauf hingearbeitet, so lange darauf gewartet. Ich meine, als du sie konfiguriert hattest, wussten wir nichtmal, dass der andere existiert. Und die Uhr passt immer zu dir. Die Farben, das Aussehen, der Wert. Alles passt davon irgendwie zu dir und es wirkt einfach nicht falsch.",
         "bild": "48_Rolly.jpg"},
{"datum": "09.11.2023",
         "titel": "You at Me",
         "text": "Du, kurz vor deinem Geburtstag bei mir. Und ich glaube, du hattest einfach auf mich gewartet, weil ich auf der Arbeit war. Und weißt du was? Ich glaube im Nachhinein, dass sowas das schönste ist, was ich mir vorstellen kann. Nach Hause zu kommen und du bist da. Egal was dann war, du machst meinen Tag um das 1000-fache besser. Von dir in den Arm genommen werden, wenn ich nach Hause komme. Mit dir reden, mit dir den Abend verbringen. Egal was, mit dir ist und war dann alles immer direkt besser. Ich vermisse das so sehr..",
         "bild": "49_You_at_me.jpg"},
{"datum": "26.11.2023",
         "titel": "Neue Couch",
         "text": "Die neue Couch war da und Emily musste sie natürlich direkt für sich einnehmen. Und auch, wenn ich am Anfang irgendwie nicht so der Fan davon war, alles umzustellen, damit es passt, muss ich am Ende zugeben: Du hattest Recht. Alles ist so viel besser mit der Couch und der Umstellung des Raums. Und es tut mir leid, dass ich das nicht immer direkt sehe und auch auf meine Meinung dann ein bisschen festgefahren bin. Aber am Ende muss ich immer wieder zugeben, dass deine Ideen mehr Sinn ergeben und einfach besser sind. Es tut mir wirklich leid, dass ich es dir in solchen Sachen immer schwerer gemacht habe, als es hätte sein sollen",
         "bild": "50_neue_Couch.jpg"},
{"datum": "02.12.2023",
         "titel": "Winter Fotoshoot",
         "text": "Unser kleines Fotoshooting im Winter beim japanischen Garten. Einfach wieder, wenn ich dieses Bild anschaue und sehe wie süß du aussiehst, bin ich wieder so glücklich, dass ich mit dir zusammen sein konnte. Auch wenn wir an dem Tag ein bisschen ausgesehen haben, als wären wir ein paar Jahre jünger geworden über Nacht, fänd ich die Vorstellung auch schön, dich schon länger gekannt zu haben. Es hat sich auf jeden Fall immer so angefühlt, als würden wir uns schon ewig kennen",
         "bild": "51_Photoshooting_Winter.jpg"},
{"datum": "07.12.2023",
         "titel": "Weihnachtsmarkt",
         "text": "Ich weiß gar nicht, war das das erste Mal, dass wir wirklich auf dem Düsseldorfer Weihnachtsmarkt waren? Aber auf jeden Fall haben wir direkt die Foto-Booth gefunden und mussten ein paar Bilder machen😂 Und ich bin mal wieder sehr froh, dass wir das gemacht haben. Die Bilder sind so toll und jedes Mal wenn ich diese Bilder in meinem Schrank sehe, denke ich an unsere Zeit zurück. Und wie schön diese ganzen Tage waren. Leider haben wir letztes Jahr kein Bild auf dem Weihnachtsmarkt in Düsseldorf gemacht, aber ich hoffe, dass wir das nochmal nachholen können. Ich hoffe es wirklich sehr",
         "bild": "52_Weihnachtsmarkt.jpg"},
{"datum": "22.12.2023",
         "titel": "Zettel auf dem Nachttisch",
         "text": "Du bist dann für Weihnachten wieder nach Münster gefahren, aber hast mir diesen Zettel zurückgelassen. Bis heute auch mein Lesezeichen. Diese Zettel von dir hab ich immer geliebt. So eine kleine Geste und doch hat es immer so viel in mir ausgelöst. Ich musst immer direkt schmunzeln, wenn irgendwo ein Zettel lag, der irgendwas kleines, süßes da stehen hatte. Und ich habe sie alle aufbewahrt und werde sie nie vergessen. Ich vermisse dich ganz schrecklich dolle!!",
         "bild": "53_Nachttische.jpg"},
{"datum": "25.12.2023",
         "titel": "Zweites Weihnachten in Münster",
         "text": "Weihnachten in Münster: Das ist irgendwie immer das schönste an Weihnachten. Es mit dir zu feiern. Deine Freude zu sehen, wenn du die kleinen Geschenke auspackst. Wenn du siehst, dass ich mir was für dich ausgedacht habe. Und auch der Abend dann mit deiner Mom und Christoph. Es war immer so schön und ich hoffe sehr, dass ich sowas noch ein paar Mal öfter erleben darf. ",
         "bild": "54_zweites_Weihnachten.jpg"},
{"datum": "31.12.2023",
         "titel": "Zweites Silvester",
         "text": "Unser zweites Silvester bei mir. Und da nicht in so einer großen Gruppe, sondern nur mit unserer Gang 😂 Aber auch so war es super schön, wenn nicht sogar noch schöner, als in so einer großen Runde. Weil wir zu viert irgendwas machen konnten und niemand uns da irgendwie gestört hat. Die Bilder sind einfach so toll und ich denke sehr gerne an diese Tage zurück.",
         "bild": "55_zweites_Silvester.jpg"},
{"datum": "17.01.2024",
         "titel": "Schneemann",
         "text": "Willkommen in 2024. Willkommen zum ersten Mal richtig Schnee für uns beide. Und wir haben es direkt genutzt, wir haben einen Schneemann gebaut. Ist er nicht cool? Es hat so Spaß gemacht mit dir im Schnee irgendetwas zu machen und auch danach wo wir noch den Berg runtergeschlittert sind. Auch wenn der Schlitten das nicht ganz so gut ausgehalten hat. Und ich möchte so gerne mit dir noch häufiger im Schnee Schneemänner bauen oder den Hang runterrollen. Egal, ob das heißt, dass es hier schneien muss oder ob wir uns nicht Richtung Schnee bewegen. Im Winter nach Finnland oder so? Da hätte ich Lust drauf.",
         "bild": "56_Schneemann.jpg"},
{"datum": "17.01.2024",
         "titel": "Lieblingsbild",
         "text": "Ich weiß gar nicht, ob ich es dir je gesagt habe. Und wenn ich so drüber nachdenke, ist das wieder so etwas, woran ich an mir selber arbeiten muss. Aber das hier ist glaube ich mein Lieblingsbild von dir. Keine Ahnung, jedes Mal wenn ich dieses Bild sehe, muss ich Lächeln und bin einfach glücklich. Du siehst so süß aus, wie du den Schneeball hältst und wie glücklich du bist. Jedes Mal freue ich mich so dieses Bild zu sehen und jedes Mal wenn ich das sehe, verliebe ich mich weiter in dich. Es ist so toll. Du bist einfach so toll.",
         "bild": "57_Lieblingsbild.jpg"},
{"datum": "18.01.2024",
         "titel": "Sometimes Crazy",
         "text": "Und hier haben wir wieder ein Beispiel, wie witzig du manchmal sein kannst 😂. Ich glaube entweder hattest du mir das Bild einfach so geschickt oder mit meinem Handy gemacht, was noch im Bad lag. Aber als ich das dann gesehen hatte, musste ich einfach nur Lachen. Das ist die Art an dir, in die ich mich verliebt habe. Deine süße, witzige und auch ein bisschen verrückte Seite. Bitte bleib immer so wie du bist, denn so bist du perfekt.",
         "bild": "58_Goofy.jpg"},
{"datum": "17.02.2024",
         "titel": "Amsterdam",
         "text": "Unser erster richtiger Städtetrip. Nach Amsterdam. Und auch wenn wir nicht unglaublich spannende Sachen gemacht haben, war es so schön, mit dir durch die Stadt zu laufen und uns alles anzuschauen. Auch der Tag danach, als wir dann in diesem Licht-Planetarium waren. Das war so cool und ich bin wirklich froh, dass wir das gemacht haben. Und schau doch bitte mal, wie süß du da aussahst. Wow, einfach Wow. Ich würde so gerne mit dir noch weitere Städtetrips machen und ich verspreche dir, dass ich auch selber was planen werde, was wir dann machen können.",
         "bild": "59_Amsterdam.jpg"},
{"datum": "20.02.2024",
         "titel": "Karneval 2024",
         "text": "Karneval 2024. Zum Glück sehr viel schöner, als das Karneval davor. Es ist immer so schön gewesen, dass du bei der Party dann dabei warst. Und dein Kostüm war auch ziemlich cool. Bisschen unfair, dass du am Ende nicht gewonnen hast. Aber wie hätten wir das dann erklären sollen 😅 Aber wir beide zusammen an Karneval, ein bisschen feiern und Spaß haben. Ich hab mich wirklich sehr darauf gefreut in den nächsten Jahren dann mit dir und den anderen Karneval in Düsseldorf zu feiern. Ich glaube, das wäre sehr cool gewesen",
         "bild": "60_Karneval_2024.jpg"},
{"datum": "30.03.2024",
         "titel": "Borkum",
         "text": "Borkum. Zählt das als Städtetrip?👀 Ich denke nicht, aber es war auch so schön, dass wir da von deiner Mom eingeladen wurden mitzukommen. Es war auch so unglaublich schön mit dir da durch die Dünen zu laufen, dir zuzusehen, wie du reiten warst und einfach mal so einen kleinen Trip zu machen. Ich hätte wahrscheinlich niemals gedacht, dass ich sonst mal auf Borkum landen würde. Wir waren ja wirklich nicht die Zielgruppe 😂 Aber das war egal, wir haben das Beste draus gemacht und es war so eine schöne Zeit",
         "bild": "61_Borkum.jpg"},
{"datum": "30.03.2024",
         "titel": "Mehr Borkum",
         "text": "Zwar hast du irgendwie immer gesagt, dass wir auf dem Bild eher wie Geschwister aussehen, aber ich mag es irgendwie trotzdem. Es sieht so einfach aus. Wir sind einfach happy und machen irgendwas, woran wir Freude haben. So wie es doch sein sollte. So wie wir immer sein wollten. Es ist und war immer so toll mit dir solche Bilder zu machen, wo wir nicht wirklich überlegt haben, sondern einfach nur Spaß haben wollten.",
         "bild": "62_Borkum_2.jpg"},
{"datum": "30.03.2024",
         "titel": "Borkum zu viert",
         "text": "Und das Bild wollte ich noch mit reinnehmen, weil es einfach toll ist. Es war so eine schöne Erfahrung wieder mit den beiden zusammen dahin zu fahren, immer mal wieder was zu machen, aber auch selber mal durch die Gegend laufen zu können. Ich hab mich wirklich sehr auf noch mehr solcher Events und Reisen gefreut. Es wäre bestimmt schön gewesen.",
         "bild": "63_Borkum_together.jpg"},
{"datum": "25.05.2024",
         "titel": "Battle-Kart",
         "text": "Battle Kart in Köln. Das war schon auch witzig. Auch wenn es immer bisschen Schade war, dass die Karts angehalten haben, wenn man ein bisschen zu nah an jemandem war. Aber eins können nur wir beide sagen an dem Tag. Wir haben gewonnen. Und ich glaube, dass zeigt dann auch einfach, dass wir beide Skill haben und im Kartfahren einfach besser sind als die anderen. Eine andere Erklärung kann ich mir nicht vorstellen. Wir müssten das wahrscheinlich nochmal testen. Weil einmal ist Glück, zweimal ist dann Können.",
         "bild": "64_Battle_Kart.jpg"},
{"datum": "30.05.2024",
         "titel": "Alicante",
         "text": "Der nächste Trip den wir zusammen gemacht haben. Es ging diesmal nach Alicante. Etwas, dass ich vorher auch gar nicht kannte. Das ist irgendwie auch immer so cool, dass ich mit dir immer irgendwas neues entdecken konnte. Ich wünschte, dass ich dir auch sowas zeigen könnte. Aber ich würde gerne noch mehr mit dir sehen. Aber jedenfalls war Alicante echt schön und ich glaube wir haben die Zeit wieder gut genutzt. Natürlich war das mit dem Schlüssel am Ende ein bisschen doof, aber naja, sowas passiert dann denke ich und ich finde, dass hat uns auch gezeigt, dass wir (oder auch ich) zusammen auch mal was blödes machen können und es trotzdem gut hinbekommen.",
         "bild": "65_Alicante.jpg"},
{"datum": "31.05.2024",
         "titel": "Karting in Alicante",
         "text": "Was immer so ein bisschen dazu gehört ist in einem Urlaub Kart zu fahren. Und am meisten macht es mir Spaß, wenn wir zusammen auf der Strecke sein können. Es ist immer so schön, wenn ich sehe, dass du bei etwas Spaß hast, was mir auch Spaß macht. Und ich glaube, dass mit ein paar mehr Runden unsere Zeiten sehr viel näher aneinander wären, als es manchmal scheint. Weil du eigentlich wirklich gut bist. Übung ist in den Dingern nur leider immer echt teuer🥹",
         "bild": "66_Kart.jpg"},
{"datum": "09.06.2024",
         "titel": "Photobooth",
         "text": "Hier waren wir in dieser Photobooth bei der Fresenius zusammen mit Aleyna und Semi. Das war auch echt witzig, auch wenn die Party da jetzt nicht so abgegangen ist. Aber einfach zusammen da was zu machen und dahin zu gehen, war sehr schön und auch lustig. Aber die Bilder sind auch echt wild geworden. Vor allem die von uns vier mit diesen ganzen Utensilien. Ich mag die Fotos sehr, sie zeigen wieder, wie viel Spaß wir hatten.",
         "bild": "67_Photobooth.jpg"},
{"datum": "01.07.2024",
         "titel": "Krankenhaus 2",
         "text": "Und da sind wir mal wieder im Krankenhaus. Zwischendurch waren wir ja mal für mich, aber du musstest ja wieder in Führung gehen (hab ich dann Ende des Jahres ja wieder ausgeglichen). Aber wie ich schon gesagt habe, ich bin einfach froh, wenn ich für dich da sein kann und dir helfen kann, dass es dir wieder besser geht. Du konntest da ja nicht so gut atmen und sowas macht mir dann ein bisschen Angst, wenn es dir nicht gut geht. Ich möchte immer, dass du gesund bist und dass du dich gut fühlst. Und ich hoffe sehr, dass ich weiterhin für dich da sein darf, wenn es dir nicht gut geht",
         "bild": "68_Krankenhaus_2.jpg"},
{"datum": "10.07.2024",
         "titel": "EM 2024",
         "text": "EM 2024 in Düsseldorf. Als wir die Spiele dann beim Public Viewing geschaut haben. Das war auch echt cool. Vor allem dann auf dem Burgplatz das Halbfinale, auch wenn Deutschland nicht mehr dabei war. Leider hatte ich kein Bild von uns beiden, sondern nur eins mit Lara und dir, aber ich hab zwischendrin noch ein kleines Selfie gemacht 😂. Es war einfach schön mit dir diese Spiele zu schauen und zu sehen, dass dir Fußball auch so Spaß macht. Ich hoffe, dass wir auch die WM so zusammen schauen können",
         "bild": "69_EM_2024.jpg"},
{"datum": "10.07.2024",
         "titel": "EM 2024 auch mit mir",
         "text": "Und hier ist das Selfie, was ich währenddessen gemacht habe 😂 Nur damit ich auch noch dazugehöre.",
         "bild": "70_EM_2024(2).jpg"},
{"datum": "19.07.2024",
         "titel": "Kirmes in Düsseldorf",
         "text": "Hier waren wir zusammen mit deinem Papa und Alex auf der Kirmes. Und ich durfte mal wieder ein paar Nahtoderfahrungen erleben. Aber für dich mach ich das irgendwie trotzdem gerne, weil ich weiß, dass es dir viel Spaß macht. Und am Ende isses meistens ja auch gar nicht so schlimm gewesen, wie man sich es meist vorstellt. Ein bisschen wie fliegen. Und dann sind wir noch auf die Brücke gegangen und wir haben uns das Feuerwerk zusammen angeschaut. Das war auch schön, als wir nebeneinander auf dieser Erhöhung standen. Bald ist die Kirmes glaub ich auch wieder. Ich würde mich so freuen mit dir dahin gehen zu können.",
         "bild": "71_Kirmes.jpg"},
{"datum": "27.07.2024",
         "titel": "Schlafi Schlafi Shirt",
         "text": "Bei dem Bild warst du schon in Italien, aber du hattest das Schlafi Schlafi Shirt dabei. Als ich das gesehen hatte, musste ich dir einfach eins holen. Und ich hoffe auch, dass du dich darüber gefreut hast. Keine Ahnung, jedes Mal wenn ich diesen Hamster sehe, muss ich sofort an dich denken, weil du den dann auch ein paar Mal benutzt hattest, sowohl als Sticker, als auch einfach so geschrieben hast mit dem i. Obwohl man ja sagen muss: Wir haben schon vor dem Hamster Sachen verniedlicht. Eigentlich sind wir die Trendsetter",
         "bild": "72_Schlafi_Schlafi.jpg"},
{"datum": "23.08.2024",
         "titel": "Mallorca 2024",
         "text": "Mallorca 2024. Insgesamt war es ein sehr schöner Urlaub, auch wenn ich mir ein bisschen mehr Zeit mit dir alleine gewünscht habe. Und es tut mir mal wieder leid, dass ich die Situation nicht so gut gehandelt habe, wie ich es hätte tun sollen. Aber trotzdem hatten wir ein paar schöne Momente. Die Bootstour, der Besuch beim Mega-Park oder die Speedboat-Tour am Ende von Madis Aufenthalt. Ich denke trotzdem sehr gerne an diese Zeit zurück und es war so schön, vor allem mit dir, diese Sachen zu erleben.",
         "bild": "73_Bootstour_Mallorca_2024.jpg"},
{"datum": "24.08.2024",
         "titel": "Ballermann",
         "text": "Der Tag im Mega-Park war auch sehr lustig. Ich meine, du hast SDP vor Leuten gerappt, die schon so kein deutsch konnten 😂 (Sorry, da hab ich dich reingeritten). Aber trotzdem fand ich den Tag echt schön und endlich warst du auch mal am Ballermann. Auch wenn mir mittlerweile wahrscheinlich ein Tag reichen würde. Aber es hat trotzdem Wiederholungsbedarf",
         "bild": "74_Mega_Park.jpg"},
{"datum": "29.08.2024",
         "titel": "Wir beide",
         "text": "Ein weiteres Hintergrundbild. Und wir sehen darauf so gut zusammen aus. Ich finde das Bild wirklich sehr schön und auch der Abend war generell echt schön. Einfach da so ein bisschen in diesem Restaurant sitzen und ein bisschen quatschen. Und die Fotos, die wir da dann von allen gemacht haben, waren auch sehr gut. Auch wenn wir ein bisschen beobachtet wurden von ein paar Gästen da 😂 Das wäre glaube ich echt ein schöner Platz, um auch mal während des Tages da zu sein, da es da dann ja auch ein paar Liegen gab.",
         "bild": "75_Mallorca_2024.jpg"},
{"datum": "03.09.2024",
         "titel": "Soller",
         "text": "Ich glaube dieser Tag war der schönste Tag des Urlaubs. Auch wenn das Wetter nicht so ganz mitgespielt hat, waren es einfach nur wir beide. Und es war so witzig. Wie wir durch den Regen laufen mussten. Wie wir das mit dem Eis gemacht haben. Wie du auf einmal random 20€ gefunden hast 😂 Alles an dem Tag war so unglaublich schön. Da sieht man, dass man nicht immer gutes Wetter braucht um einen wunderschönen Tag zu haben. Wir hatten wirklich so viel Spaß. Ich bin sehr froh, dass das Wetter uns da mal ein Strich durch die Rechnung gemacht hat. Einer meiner Lieblingstage, die ich je hatte",
         "bild": "76_Soller(1).jpg"},
{"datum": "03.09.2024",
         "titel": "Parkhaus in Soller",
         "text": "Hier nochmal das Bild aus dem Parkhaus. Wie wir so dachten „Ja wenn wir jetzt loslaufen wird das bestimmt was“ und es dann doch irgendwie immer schlimmer wurde. Die Straßen waren schon richtig überflutet. Zum Glück haben wir es noch aus dem Parkhaus und auf den Weg nach Hause geschafft. Aber es war wirklich so ein lustiger Tag. Ich denke wirklich sehr gerne daran zurück. Ich hoffe, du auch.",
         "bild": "77_Soller(2).jpg"},
{"datum": "03.09.2024",
         "titel": "2 Jahre",
         "text": "Und um den Tag perfekt zu machen, hatten wir auch noch unser zweijähriges in diesem schicken Steak-Restaurant gefeiert. Das war auch echt schön. Und da ist dann auch mein zweites Lieblingsbild von dir entstanden. Immer wenn du mich anrufst oder ich dich anrufe sehe ich dieses Bild und es ist so wunderschön. Du bist so wunderschön. Und immer wieder, wenn ich an diesen Tag denke, wird mir wirklich warm ums Herz. Ich bin so unendlich dankbar, dass der Tag so gelaufen ist, wie er war. Und ich könnte mir nichts Besseres vorstellen. Es war wirklich so schön. Wirklich, ich hoffe so sehr, dass wir noch weitere solcher Tage haben dürfen",
         "bild": "78_2_Years.jpg"},
{"datum": "04.09.2024",
         "titel": "Us together",
         "text": "Ich glaube es war unser letzter Abend auf Mallorca für dieses Jahr und wir sind nochmal rausgegangen, ein bisschen durch die Gegend spaziert, waren was essen und waren einfach zusammen. Ich glaub, das ist wirklich meine Wohlfühlzone. Mit dir zusammen sein und durch die Gegend laufen und dann was essen gehen. So ganz normale Sachen. Aber mit dir ist dann alles so special. Einfach besser als alles andere. Und ich würde so gerne mit dir nochmal durch die Gegend laufen und deine Hand nehmen. Mit dir spazieren, über irgendetwas reden und am Ende mit dir zusammen auf die Couch setzen und ein bisschen kuscheln. Ich vermisse das wirklich so sehr.",
         "bild": "79_Us_together.jpg"},
{"datum": "04.09.2024",
         "titel": "Noch mehr wir",
         "text": "Ich wollte auch noch dieses Bild mit reinbringen. Da sehen wir auch so gut zusammen aus. Zu gut, um nicht noch weitere solcher Bilder zu machen. Wir haben da eine neue Pose gelernt, die wir dann auch später nochmal ausprobiert hatten, als uns diese älteren Frauen fotografiert hatten. Da hat es dann aber nicht ganz so gut funktioniert 😂. Aber das Bild sehe ich trotzdem noch täglich auf meinem Handyhintergrund und ich finde es immer wieder schön. Ich vermisse es Bilder mit dir zu machen.",
         "bild": "80_us_together(2).jpg"},
{"datum": "02.10.2024",
         "titel": "Jonas Brothers",
         "text": "Wir waren mal wieder zu zweit auf einem Konzert. Wir waren bei den Jonas Brothers. Am Ende haben wir gemerkt, dass das doch nicht so wirklich was für uns war, aber es war trotzdem irgendwie ganz cool da zu sein. Ein paar Songs kannte man dann ja doch. Aber insgesamt war es sehr schön etwas zu machen. Du bist gerade neu in die Uni gestartet und hattest natürlich viele neue Eindrücke. Und dann war so eine kleine Abwechslung einfach mal wieder schön.",
         "bild": "81_Jonas_Brothers.jpg"},
{"datum": "12.10.2024",
         "titel": "Oktoberfest",
         "text": "Oktoberfest in Münster. Davon hattest du immer so viel erzählt und es hat nicht enttäuscht. Auch wenn wir nächste Mal vielleicht wirklich Plätze suchen sollten 😂. Aber wir hatten ja Glück. Und der Abend war einfach wieder sehr lustig. Vor allem dann mit dir und den anderen beiden. Solche Tage finde ich wirklich immer wieder schön. Und auch danach in diesem Club, wie hieß der nochmal? Die Musik war echt gut und es hat wirklich sehr viel Spaß gemacht zu viert dahin zu gehen. Ich hoffe, wir können das nochmal machen",
         "bild": "82_Oktoberfest.jpg"},
{"datum": "26.10.2024",
         "titel": "Topgolf 2",
         "text": "Eine weitere Runde Topgolf. Und sind wir etwas besser geworden? Ich weiß es nicht. Vielleicht ein bisschen. Aber ich glaube Golfer werden wir so schnell nicht. Das müssen wir aber nicht. Du hast in dem einen Spiel irgendwann herausgefunden, wie man am meisten Punkte macht und hast das dann einfach schamlos ausgenutzt 😂. Ich glaub ich war auch der Einzige, der keine Runde gewonnen hat. Aber das ist auch nicht schlimm. Ich sehe lieber dich gewinnen, als selber zu gewinnen. Weil du dann immer so glücklich bist. Und ich hoffe sehr, dass ich nochmal hören kann, wie du mir erzählst, dass du ja gewonnen hast und deswegen die Beste bist 😂",
         "bild": "83_Topgolf_2.jpg"},
{"datum": "31.10.2024",
         "titel": "Halloween",
         "text": "Hier sind wir nun auf der Halloween Party. Die war auch echt cool. Also vor allem der Abend erstmal bei Lara. Da hatte ich dann auch viel Spaß. Auch wenn der Club am Ende nicht soo unsere Musik war (finde ich), war es ja trotzdem mal wieder schön mit ein paar Leuten wegzugehen. Aber einfach zusammen so ein Paar-Kostüm zu haben, fand ich sehr schön. Zwar war es jetzt nicht das Aufwendigste, aber das muss es ja auch nicht immer sein. Wir haben ja trotzdem den Kostümwettbewerb gewonnen 😂 Ich glaube ich habe nie was vom Preis bekommen, naja, nicht so schlimm",
         "bild": "84_Halloween.jpg"},
{"datum": "31.10.2024",
         "titel": "Kuss an Halloween",
         "text": "Und dann haben wir ja noch dieses Bild. Das ist auch sehr schön. Da hatte Caro glaube ich einen sehr guten Einfall, wie wir das Bild machen sollten. Ich finde wirklich, das sieht so gut aus. Es könnte auch eine Werbung sein. Wir sind halt wirklich einfach ein sehr gutes Team. Ich hoffe, dass du das auch wieder sehen kannst.",
         "bild": "85_We_Halloween.jpg"},
{"datum": "04.11.2024",
         "titel": "You & Emily",
         "text": "Meine beiden liebsten Lebewesen zusammen. Du und Emily. Wenn nicht gerade Zeckensaison ist, seid ihr beide wirklich sehr süß miteinander und ich bin immer wieder sehr froh, dass du dich irgendwann mit Emily anfreunden konntest. Vielleicht hat dich das ein bisschen dazu verleitet, dass du Katzen auch ein bisschen mehr magst, als vorher. Weil ihr beiden seid schon einfach sweet. Auch wenn du sie ein bisschen mit deiner Liebe erdrückst 😂",
         "bild": "86_My_Loves.jpg"},
{"datum": "11.11.2024",
         "titel": "Happy 24",
         "text": "Dein 24. Geburtstag. Und es war sehr schön, dass wir den mit Lara und Aleyna zusammen feiern konnten. Ich glaube auch, dass du dich gefreut hast. Und es war schön für dich ein bisschen dekorieren zu können, so wie du es im Vorjahr für mich gemacht hast. Ich bin wirklich immer sehr froh, dass ich bei solchen Sachen dabei sein durfte. Einfach bei dir zu sein, bei deinen wichtigsten Events, ist so schön und macht mich immer so glücklich.",
         "bild": "87_Happy_24.jpg"},
{"datum": "15.11.2024",
         "titel": "Schießen",
         "text": "Etwas, was ich auch nie dachte, dass ich das mal machen kann. Wir waren auf dem Schießstand und haben uns glaube ich besser geschlagen, als wir es erwartet hatten. Und es war schon eine coole Erfahrung. Bisschen beängstigend, aber nach ner Zeit wirklich sehr cool. Wäre echt schön, wenn wir das nochmal mit anderen Waffen ausprobieren könnten. Ich glaub mit denen wärst auch du nochmal wesentlich besser. Ich würde mich freuen.",
         "bild": "88_Shooting.jpg"},
{"datum": "24.11.2024",
         "titel": "Berlin",
         "text": "Ja Berlin, was soll man dazu sagen? Keine Ahnung. Es war nicht der Ausflug, den wir uns gewünscht haben. Und das ist mit großem Anteil meine Schuld. Und es tut mir wirklich sehr leid. Ich weiß nichtmal genau, warum ich da so gereizt reagiert hatte. Oder wieso ich einfach nicht so hundertprozent glücklich war. Ich wollte, dass der kurze Trip schön wird. Dass du Ludovico Einaudi sehen kannst und wir dabei noch so ein bisschen was erleben. Berlin ist vielleicht aber auch wirklich nicht unsere Stadt. Aber wenn ich die Zeit nochmal zurückdrehen könnte, würde ich das sehr gerne machen. Dir einfach einen schönen Trip bescheren. Es tut mir wirklich leid. Es würde nicht nochmal vorkommen, wenn du mit mir nochmal wohin fahren wollen würdest.",
         "bild": "89_Berlin.jpg"},
{"datum": "31.12.2024",
         "titel": "Silvester 2024",
         "text": "Silvester Nummer 3. Und ich glaube, das war echt eigentlich ganz schön. Wir haben zusammen Bilder gemacht, Bierpong gespielt und wir waren wieder mal für einander da während der Umstellung auf das neue Jahr. Einfach nur, dass du da wieder dabei warst und wir uns gegenseitig zuerst ein frohes neues Jahr gewünscht haben, macht diesen Tag immer so toll. Ich bin wirklich sehr glücklich und dankbar, dass du immer wieder mit mir zusammen gefeiert hast. Das ist wirklich nicht selbstverständlich. Danke, einfach danke ❤️",
         "bild": "90_Silvester_2024.jpg"},
{"datum": "26.01.2025",
         "titel": "Unsere Zukunft",
         "text": "Das neue Jahr beginnt und wir planen zusammenzuziehen. Und auch hier muss ich mich als erstes nochmal entschuldigen und meine Fehler eingestehen. Ich hätte dir direkt zeigen sollen, wie sehr ich mich darauf freue mit dir zusammenzuziehen. Das habe ich nicht so gemacht, wie du es verdient hattest. Bei mir spielte da natürlich auch ein bisschen die Angst einer neuen Zukunft mit, einer großen Veränderung, aber das ist keine Ausrede und auch kein Grund, sich manchmal so quer zu stellen. Heutzutage würde ich mir gerne nochmal sagen können, dass ich dir mehr zeigen soll, wie sehr ich mich auf eine Zukunft mit dir freue. Vielleicht hätte dir das ein besseres Gefühl gegeben. Aber leider habe ich es dir zu spät gesagt. Es tut mir wirklich leid. Ich wünsche mir wirklich so sehr, dass wir es vielleicht doch noch irgendwann schaffen eine gemeinsame Zukunft mit zusammenziehen und einer glücklichen Beziehung haben können. Das ist wirklich mein größter Wunsch. Wir beide, zusammen, dass wir einfach viel erleben und schaffen können. Bitte, kannst du mir das noch erfüllen?",
         "bild": "91_Our_Future_pls.jpg"},
{"datum": "22.03.2025",
         "titel": "Just You",
         "text": "Nach meiner OP war ich länger nicht mehr in Düsseldorf, aber an diesem Tag war ich das erste Mal wieder bei dir. Weil wir ins Möbelhaus fahren wollten, zu Hoeffner. Und ich hatte dich da gesehen und wollte einfach ein Bild von dir machen. Weil du so hübsch da aussahst und irgendwie lächeln musstest. Ich weiß nicht genau weswegen, aber es hat mich so glücklich gemacht und dann habe ich das Bild gemacht. Ich mag es sehr, ich weiß nicht was du dazu sagst.",
         "bild": "92_just_you.jpg"},
{"datum": "07.04.2025",
         "titel": "Pancake",
         "text": "Ich glaube ich werde nie den Moment vergessen, wie glücklich du warst, als du Pancake ausgepackt hast. Ich war so happy, dass du dich so gefreut hast. Für einen Moment hab ich gedacht, dass ich der glücklichste Mensch auf der Welt bin. Also abgesehen von dir, weil du so Spaß an Pancake hattest. Und dass du mir dann immer abends den Pancake Sticker geschickt hast, das war wirklich das schönste. Es hatte so eine unglaubliche Bedeutung für mich, weil es nicht einfach nur ein Herz war, sondern was Persönliches. Was, das nur wir haben. Etwas, was uns beide so glücklich macht. Ich hoffe so sehr, dass ich dich nochmal so glücklich machen kann. Und nicht nur einmal, sondern so oft es nur geht 🥞.",
         "bild": "93_Pancake.jpg"},
{"datum": "26.04.2025",
         "titel": "Our last Pic?",
         "text": "Unser letztes Bild.. Es tut wieder so weh das zu sehen und das hier jetzt zu schreiben. Ich habe mir auf dieser Hochzeit so sehr gewünscht, dass wir das auch irgendwann haben können. Ich habe dich während der gesamten Trauung angeschaut und mir vorgestellt, wie es mit dir wäre. Und ich dachte einfach nur, dass es wunderschön wäre. Was ich alles dafür tun würde, irgendwann die Chance zu haben, dich zu heiraten. Mit dir eine Zukunft aufzubauen. Eine Familie zu haben. Das wäre so ein schönes Leben, ein besseres hätte ich mir nie vorstellen können. Deswegen tut es umso mehr weh, dass das unser letztes Bild ist. Und ich hoffe so sehr, dass es nicht das letzte bleiben wird. Sondern, dass wir noch viel mehr Bilder machen können, die irgendwann in diesem Zeitstrahl angehangen werden können. Ich bitte dich so sehr darum, dass du uns diese Möglichkeit gibst. Bitte. Ich liebe dich❤️🥞",
         "bild": "94_Our_last_Pic.jpg"}
    ]

# Seiteneinstellungen und Layout
st.set_page_config(page_title = "Unsere App", layout = "wide")

# Seitenleiste mit Menü-Navigation
auswahl = st.sidebar.radio("Menü", ["❤️Start", "⏰Zeitstrahl", "📍Aktivitäten in unserer Nähe", "🥘Rezepte-Planer"])

def get_github_bild_url(dateiname):
    return f"https://raw.githubusercontent.com/Quanduu97/website-project/main/bilder/{dateiname}"


# Funktionen für die verschiedenen Seiten
def zeige_start():
    
    # Überschrift der Seite
    st.markdown("""
                <h1 style = 'color: #ffffff;'> 💌 Willkommen auf unserer Seite 🥞 </h1>""", unsafe_allow_html=True)
    st.markdown("""
                Ich hoffe es gefällt dir. Ich versuche hiermit ein paar unserer Momente zu zeigen und auch meine Fehler zu verbessern. 
                Ein bisschen eine Unterstützung für mich und uns, damit ich es für uns besser machen kann. ❤️""")
    
    # Info-Text
    st.info("""Kleine Info - ich bin noch nicht komplett fertig, aber ich wollte dir schonmal zeigen, an was ich weiterarbeiten werde :)
            \nIch weiß auch, dass du gerade Abstand haben möchtest. Aber vielleicht zeigt dir das ein wenig, dass ich mich wirklich reinhängen möchte\n
            \nIch glaube so sehr an uns 🥹\n""")
    
    # Seitentrenner
    st.markdown("---")

    # Diashow der Zeitstrahl-Fotos
    st.markdown("""
                <h1 style = 'color: #ffffff;'> Hier sind ein paar unserer schönsten Momente ❤️ </h1>
                Diese ganzen Momente findest du auch auf dem Zeitstrahl. Hier sind sie in einer Diashow angeordnet""", unsafe_allow_html=True)

        # Liste aller Bild-URLs aus dem Zeitstrahl
    bilder_urls = [get_github_bild_url(eintrag["bild"]) for eintrag in zeitstrahl]

    # HTML, CSS & JS für Slideshow mit Fade-Effekt & angepasstem Bild-Styling
    html_code = f"""
    <style>
    .slideshow-container {{
        max-width: 600px;
        position: relative;
        margin: auto;
	height: auto;
    }}
    .mySlides {{
	display: none;
    	width: 100%;
    	height: auto;
    	max-height: 80vh;
    	object-fit: contain;
    	border-radius: 12px;
    	box-shadow: 0 0 12px rgba(0,0,0,0.3);
    	margin-bottom: 20px;
    }}
    @keyframes fade {{
        from {{ opacity: 0.4 }} 
        to {{ opacity: 1 }}
    }}
    </style>

    <div class="slideshow-container">
        {"".join([f'<img class="mySlides" src="{url}" />' for url in bilder_urls])}
    </div>

    <script>
    let slideIndex = 0;
    showSlides();
    function showSlides() {{
        let slides = document.getElementsByClassName("mySlides");
        for (let i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
        }}
        slideIndex++;
        if (slideIndex > slides.length) {{ slideIndex = 1 }}
        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 3000); // alle 3 Sekunden wechseln
    }}
    </script>
    """

    html(html_code, height=600)
	


def zeige_zeitstrahl():
    st.title("Zeitstrahl")
    st.info("""Hello ❤️ \
    \n\nIch habe für uns einen kleinen Zeitstrahl entworfen, der unsere gesamte Zeit etwas widerspiegelt. Ich hoffe, dass dich das ein bisschen erinnern lässt, was wir alles so gemacht haben, was wir erlebt haben, zusammen geschafft haben und warum wir so ein gutes Team sind. \
    Ich würde mich freuen, wenn du dir den ganzen Zeitstrahl durchlesen würdest. Und vielleicht ist das ein kleiner Denkanstoß, ob sich unsere Beziehung für dich und uns vielleicht doch noch lohnt. Ich hoffe es. \
    \n\nIch hoffe, dass du Spaß daran hast eine kleine Zeitreise zu erleben. Ich hatte sehr viel Spaß mir all das nochmal anzuschauen. Ich liebe dich ❤️🥞""")

   

    for eintrag in zeitstrahl:
        st.markdown(f"### {eintrag['titel']} ({eintrag['datum']})")
        bildpfad = get_github_bild_url(eintrag["bild"])
        if bildpfad:
           st.markdown(f"""
           <div style='text-align: center;'>
           <img src='{bildpfad}' style='width: 400px; border-radius: 12px; box-shadow: 0 0 12px rgba(0,0,0,0.15);' />
           </div>""", unsafe_allow_html=True)
        else:
            st.warning(f"Bild nicht gefunden: {eintrag['bild']}")
        
        st.markdown(f"""
                <div style='
                        max-width: 800px;
                        margin: 20px auto;
                        font-size: 20px;
                        text-align: center;
                        line-height: 1.6;
                                '>
                        {eintrag['text']}
                        </div>

                """, unsafe_allow_html=True)
        st.markdown("---")

# GPT-Antwortfunktion
def gpt_antwort(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein kreativer Ideenlieferant für Dates und Events."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=450
    )
    return response.choices[0].message.content

# 💡 GPT: Date-Ideen (lang = Wochenende / kurz = Abend)
def zeige_date_ideen(lang):
    st.subheader("💡 Date-Ideen")
    if lang:
        prompt = (
            "Gib mir 5 kreative, unterschiedliche Date-Ideen fürs Wochenende. Gerne in der Nähe von Düsseldorf."
            "Sie dürfen auch einen ganzen Tag oder eine Übernachtung umfassen. Eine Übernachtung darf maximal 3 Stunden von Düsseldorf entfernt sein (mit dem Auto)."
            "Gebe höchstens eine Übernachtung aus."
            "Variiere die Ideen bei jeder Anfrage."
        )
    else:
        prompt = (
            "Gib mir 5 abwechslungsreiche, kreative Date-Ideen für einen normalen Abend (ca. 2-3 Stunden). "
            "Sie sollen romantisch, witzig oder entspannend sein. "
            "Variiere die Ideen bei jeder Anfrage."
        )
    antwort = gpt_antwort(prompt)
    st.markdown(antwort)

def web_search_impl(query: str) -> dict:
    params = {
        "engine":       "google",
        "q":            f"{query} site:duesseldorf",
        "location":     "Düsseldorf, Germany",
        "api_key":      st.secrets["search"]["serpapi_key"],
        "num":          5
    }
    search = GoogleSearch(params)
    result = search.get_dict()
    snippets = []


#GPT Events in der Nähe
def zeige_events_per_gpt():
    st.info("🔎 Suche nach aktuellen Events in Düsseldorf läuft ...")

    params = {
        "engine": "google",
        "q": "aktuelle Veranstaltungen Düsseldorf site:mrduesseldorf.de OR site:eventbrite.de OR site:duesseldorf-tourismus.de",
        "api_key": serpapi_key,
        "location": "Düsseldorf, Germany",
        "hl": "de",
        "gl": "de",
        "num": 10
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    events = []

    try:
        organic_results = results.get("organic_results", [])

        for res in organic_results[:5]:
            events.append({
                "Quelle": "SerpAPI",
                "Titel": res["title"],
                "Datum": datetime.today().strftime("%Y-%m-%d"),
                "Link": res["link"]
            })

        if events:
            st.info("Leider werden hier nur die Webseiten angezeigt, auf denen man Events findet." \
            "\n \nIch habe alles versucht..")
            zeige_kalender(events)
        else:
            st.warning("Keine Events gefunden.")

    except Exception as e:
        st.error(f"❌ Fehler bei der GPT-Eventsuche: {str(e)}")


def zeige_kalender(events):
    kalender = defaultdict(list)
    for ev in events:
        kalender[ev["Datum"]].append(ev)
    for datum in sorted(kalender.keys()):
        st.subheader(datum)
        for ev in kalender[datum]:
            st.markdown(f"- **{ev['Titel']}**  → [Details]({ev['Link']})  *(via {ev['Quelle']})*")


def zeige_aktivitaetensuche():
    st.title("📍Aktivitätensuche in unserer Nähe")
    st.markdown("Hier findest du Events, Date-Ideen fürs Wochenende und spontane Abendvorschläge.")
		st.info("Hier auf dieser Seite kannst du auf einen der Buttons drücken. Dadurch werden uns Vorschläge für Events sowie Date-Ideen für Wochenenden und entspannte Abende zu zweit vorgeschlagen."\
            "\n \nNur als kleine Hilfe, falls wir mal keine Ideen haben ❤️")
						

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎉 Events in der Nähe"):
            zeige_events_per_gpt()

    with col2:
        if st.button("🌄 Date-Ideen fürs Wochenende"):
            zeige_date_ideen(lang=True)

    with col3:
        if st.button("🌙 Date-Ideen für einen Abend"):
            zeige_date_ideen(lang=False)

    st.markdown("---")
        
# Auswahl auswerten und Seite anzeigen
if auswahl == "❤️Start":
    zeige_start()
elif auswahl == "⏰Zeitstrahl":
    zeige_zeitstrahl()
elif auswahl == "📍Aktivitäten in unserer Nähe":
    zeige_aktivitaetensuche()

