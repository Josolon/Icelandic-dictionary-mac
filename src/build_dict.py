import os
import xml.etree.ElementTree as ET
from islenska import Bin

# 1. Þýðingasafn fyrir málfræðiheiti (Orðflokka)
POS_TRANSLATION = {
    "noun": "nafnorð",
    "verb": "sögn",
    "adjective": "lýsingarorð",
    "adverb": "atviksorð",
    "pronoun": "fornafn",
    "numeral": "töluorð",
    "preposition": "forsetning",
    "conjunction": "tengingarorð",
    "interjection": "upphrópun",
    "expletive": "fylliorð",
    "article": "greinir",
    "phrase": "orðasamband"
}

def decode_grammatical_tag(tag):
    """Snýr flóknum skammstöfunum BÍN yfir í nett og hefðbundin orðabókarheiti."""
    parts = []
    
    # Föll (Cases)
    if "NF" in tag: parts.append("nf.")
    elif "ÞF" in tag: parts.append("þf.")
    elif "ÞGF" in tag: parts.append("þgf.")
    elif "EF" in tag: parts.append("ef.")
    
    # Talan (Numbers)
    if "ET" in tag: parts.append("et.")
    elif "FT" in tag: parts.append("ft.")
    
    # Greinir (Article)
    if "gr" in tag: parts.append("m.gr.")
    
    # Sagnabeygingar (Verbs)
    if "FH" in tag: parts.append("fh.")
    elif "VH" in tag: parts.append("vh.")
    elif "NH" in tag: parts.append("nh.")
    
    if "NT" in tag: parts.append("nt.")
    elif "ÞT" in tag: parts.append("þt.")
    
    if "1P" in tag: parts.append("1.p.")
    elif "2P" in tag: parts.append("2.p.")
    elif "3P" in tag: parts.append("3.p.")
    
    if parts:
        return "".join(parts)
    return tag

def parse_ino_and_build_apple_xml(ino_xml_path, output_xml_path):
    print("🚀 Upphafsstilli BÍN beygingargrunninn...")
    # Slökkvum á compound hyphens svo samsett orð brotni ekki í kerfisleit macOS
    bin_engine = Bin(add_compound_hyphens=False)
    
    print(f"📖 Opna frumgögn: {ino_xml_path}")
    tree = ET.parse(ino_xml_path)
    root = tree.getroot()
    
    # Grunnrót fyrir Apple Dictionary sniðið
    apple_root = ET.Element('d:dictionary', {
        'xmlns': 'http://www.w3.org/1999/xhtml',
        'xmlns:d': 'http://www.apple.com/DTDs/DictionaryService-1.0.rng'
    })
    
    entries = root.findall('.//LexicalEntry')
    print(f"🗂️ Fann {len(entries)} færslur til úrvinnslu.")
    
    processed_count = 0
    
    for lexical_entry in entries:
        entry_id = lexical_entry.get('id', f'id_{processed_count}')
        
        # Sækjum ensku heitin og snúum þeim yfir á íslensku
        pos_feat = lexical_entry.find("./feat[@att='partOfSpeech']")
        raw_pos = pos_feat.get('val') if pos_feat is not None else ""
        pos = POS_TRANSLATION.get(raw_pos, raw_pos)
        
        lemma_feat = lexical_entry.find("./Lemma/feat[@att='writtenForm']")
        if lemma_feat is None:
            continue
        headword = lemma_feat.get('val')
        
        def_text_node = lexical_entry.find('.//SemanticDefinition/text')
        definition = def_text_node.text if def_text_node is not None else "Engin skilgreining fannst."
        
        # Búum til færsluspjaldið sjálft
        apple_entry = ET.SubElement(apple_root, 'd:entry', {
            'id': entry_id,
            'd:title': headword
        })
        
        # Aðalleitarvísir (fyrir fletta orðið sjálft)
        ET.SubElement(apple_entry, 'd:index', {'d:value': headword})
        
        # Safn til að halda utan um mörg beygingarheiti á sama formi (samföll)
        morphology_map = {}
        
        try:
            # Flettum upp í BÍN til að sækja öll beygingarformin
            _, matches = bin_engine.lookup(headword)
            seen_forms = set([headword])
            
            for match in matches:
                if match.ord == headword:
                    bin_id = match.bin_id
                    if bin_id:
                        paradigm = bin_engine.lookup_id(bin_id)
                        for row in paradigm:
                            inflected_form = row.bmynd
                            grammatical_tag = row.mark
                            
                            if inflected_form:
                                explanation = decode_grammatical_tag(grammatical_tag)
                                
                                # Ef formið hefur sést áður (samfall), bætum við nýju greiningunni við í hópinn
                                if inflected_form not in morphology_map:
                                    morphology_map[inflected_form] = set()
                                morphology_map[inflected_form].add(explanation)
                                
                                # Skráum falið leitarorð í kerfiskort Apple svo beygð form finni þetta spjald
                                if inflected_form not in seen_forms:
                                    seen_forms.add(inflected_form)
                                    ET.SubElement(apple_entry, 'd:index', {'d:value': inflected_form})
        except Exception:
            pass
            
        # --- HTML Uppsetning á Útliti Spjaldsins ---
        div = ET.SubElement(apple_entry, 'div', {
            'class': 'dict-body', 
            'style': 'font-family: -apple-system, BlinkMacSystemFont, sans-serif;'
        })
        
        # Fletta (Aðalorð)
        h1 = ET.SubElement(div, 'h1', {'style': 'margin-bottom: 2px; font-size: 1.6em;'})
        h1.text = headword
        
        # Orðflokkur (á íslensku)
        if pos:
            span_pos = ET.SubElement(div, 'span', {
                'class': 'pos-badge', 
                'style': 'color: #8e8e93; font-style: italic; font-size: 0.9em;'
            })
            span_pos.text = f" ({pos})"
        
        # Lína á milli
        ET.SubElement(div, 'hr', {'style': 'border: 0; border-top: 1px solid #e5e5ea; margin: 8px 0;'})
        
        # Skilgreining texti
        p_def = ET.SubElement(div, 'p', {'class': 'definition', 'style': 'line-height: 1.4; margin-bottom: 10px;'})
        p_def.text = definition
        
        # Notkunardæmi (ef þau eru til staðar)
        example_nodes = lexical_entry.findall('.//SenseExample/text')
        if example_nodes:
            p_ex_title = ET.SubElement(div, 'p', {'style': 'margin-top: 10px; font-weight: bold; font-size: 0.9em; color: #3a3a3c;'})
            p_ex_title.text = "Notkunardæmi:"
            ul_node = ET.SubElement(div, 'ul', {'style': 'padding-left: 15px; margin-top: 4px; color: #48484a;'})
            for ex_node in example_nodes:
                if ex_node.text:
                    li = ET.SubElement(ul_node, 'li', {'style': 'margin-bottom: 3px;'})
                    em = ET.SubElement(li, 'em')
                    em.text = f"„{ex_node.text}“"
        
        # Snyrtilegur fellilisti með nettu töfluskipulagi fyrir beygingarnar
        if morphology_map:
            details = ET.SubElement(div, 'details', {'style': 'margin-top: 14px; font-size: 0.85em;'})
            
            summary = ET.SubElement(details, 'summary', {
                'style': 'cursor: pointer; font-weight: bold; color: #007AFF; outline: none; margin-bottom: 6px;'
            })
            summary.text = "Beygingarform"
            
            # Notum CSS Grid til að fella formin í dálka í staðinn fyrir endalausan lóðréttan lista
            ul_morph = ET.SubElement(details, 'ul', {
                'style': 'list-style-type: none; padding-left: 0; margin-top: 4px; color: #555; display: grid; grid-template-columns: repeat(auto-fill, minmax(135px, 1fr)); gap: 6px;'
            })
            
            for form, explanations in sorted(morphology_map.items()):
                li_morph = ET.SubElement(ul_morph, 'li', {
                    'style': 'padding: 3px 5px; background: #f2f2f7; border-radius: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'
                })
                
                b_form = ET.SubElement(li_morph, 'b')
                b_form.text = form
                
                # Tengjum saman möguleg samföll með skástriki (" eða ")
                combined_explanations = " eða ".join(sorted(explanations))
                span_exp = ET.SubElement(li_morph, 'span', {'style': 'color: #8e8e93; font-size: 0.85em; font-weight: normal;'})
                span_exp.text = f" ({combined_explanations})"
                    
        processed_count += 1
        if processed_count % 5000 == 0:
            print(f"🔄 Samsetning orðapars: Unnið úr {processed_count} færslum...")

    print("💾 Skrifa tilbúið XML út á disk...")
    output_tree = ET.ElementTree(apple_root)
    ET.indent(output_tree, space="    ")
    
    dir_name = os.path.dirname(output_xml_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    output_tree.write(output_xml_path, encoding='utf-8', xml_declaration=True)
    print(f"🎉 Glæsilegt! Gögnin eru tilbúin til þjöppunar á: {output_xml_path}")

if __name__ == "__main__":
    source_xml = "data/ino_data.xml"
    compiled_xml = "IcelandicDictionary.xml"
    parse_ino_and_build_apple_xml(source_xml, compiled_xml)