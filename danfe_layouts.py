"""
Layouts DANFE para diferentes versões de NF-e
Salve este arquivo como danfe_layouts.py no mesmo diretório do script principal
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime

def gerar_v2(generator, output_path):
    """Layout NF-e 2.0 - Simplificado"""
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    m = 5*mm
    
    # Extração de dados
    emit_nome = generator._get_text('.//nfe:emit/nfe:xNome')
    emit_end = f"{generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xLgr')}, {generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:nro')}"
    emit_cidade = f"{generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xMun')}/{generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:UF')}"
    
    dest_nome = generator._get_text('.//nfe:dest/nfe:xNome')
    dest_doc = generator._get_text('.//nfe:dest/nfe:CNPJ') or generator._get_text('.//nfe:dest/nfe:CPF')
    dest_doc_fmt = generator._format_cnpj(dest_doc) if len(dest_doc) == 14 else generator._format_cpf(dest_doc)
    
    nf_num = generator._get_text('.//nfe:ide/nfe:nNF')
    nf_nat = generator._get_text('.//nfe:ide/nfe:natOp')
    nf_data = generator._get_text('.//nfe:ide/nfe:dEmi')
    chave = generator._get_text('.//nfe:protNFe/nfe:infProt/nfe:chNFe')
    
    tot_prod = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vProd', '0'))
    tot_frete = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vFrete', '0'))
    tot_icms = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vICMS', '0'))
    tot_nf = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vNF', '0'))
    
    y = h - m
    
    # Header
    hh = 25*mm
    c.rect(m, y-hh, 60*mm, hh)
    # c.drawCentredString(m+30*mm, y-hh/2, "[LOGO/RECIBO]")
    c.drawCentredString(m+30*mm, y-hh/2, "")
    
    c.rect(m+60*mm, y-hh, 80*mm, hh)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(m+100*mm, y-10*mm, "DANFE")
    c.setFont("Helvetica", 7)
    c.drawCentredString(m+100*mm, y-14*mm, "Documento Auxiliar da NF-e")
    
    c.rect(m+140*mm, y-hh, 60*mm, hh)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+142*mm, y-4*mm, "CHAVE DE ACESSO")
    c.setFont("Helvetica", 5.5)
    chave_f = generator._format_chave(chave)
    c.drawString(m+142*mm, y-8*mm, chave_f[:23])
    c.drawString(m+142*mm, y-11*mm, chave_f[24:])
    
    # Emitente
    y -= hh + 2*mm
    eh = 12*mm
    c.rect(m, y-eh, 140*mm, eh)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+2*mm, y-3*mm, "EMITENTE")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(m+2*mm, y-7*mm, emit_nome)
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-10*mm, f"{emit_end} - {emit_cidade}")
    
    c.rect(m+140*mm, y-eh, 60*mm, eh)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+142*mm, y-3*mm, "NATUREZA DA OPERAÇÃO")
    c.setFont("Helvetica", 7)
    c.drawString(m+142*mm, y-7*mm, nf_nat[:30])
    
    # Destinatário
    y -= eh + 2*mm
    dh = 10*mm
    c.rect(m, y-dh, 140*mm, dh)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+2*mm, y-3*mm, "DESTINATÁRIO")
    c.setFont("Helvetica", 8)
    c.drawString(m+2*mm, y-7*mm, f"{dest_nome} - {dest_doc_fmt}")
    
    c.rect(m+140*mm, y-dh, 60*mm, dh)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+142*mm, y-3*mm, "DATA EMISSÃO")
    c.setFont("Helvetica", 8)
    c.drawString(m+142*mm, y-7*mm, nf_data)
    
    # Totais
    y -= dh + 2*mm
    th = 8*mm
    c.rect(m, y-th, 40*mm, th)
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-5*mm, f"Valor Prod: {tot_prod:.2f}")
    
    c.rect(m+40*mm, y-th, 40*mm, th)
    c.drawString(m+42*mm, y-5*mm, f"Frete: {tot_frete:.2f}")
    
    c.rect(m+80*mm, y-th, 40*mm, th)
    c.drawString(m+82*mm, y-5*mm, f"ICMS: {tot_icms:.2f}")
    
    c.rect(m+120*mm, y-th, 80*mm, th)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m+122*mm, y-5*mm, f"TOTAL NF: {tot_nf:.2f}")
    
    # Produtos
    y -= th + 2*mm
    ph = 80*mm
    c.rect(m, y-ph, w-2*m, ph)
    
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-6*mm, w-2*m, 6*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-4*mm, "Cód")
    c.drawString(m+20*mm, y-4*mm, "Descrição")
    c.drawString(m+90*mm, y-4*mm, "NCM")
    c.drawString(m+110*mm, y-4*mm, "Qtd")
    c.drawString(m+130*mm, y-4*mm, "UN")
    c.drawString(m+145*mm, y-4*mm, "V.Unit")
    c.drawString(m+170*mm, y-4*mm, "V.Total")
    
    items = generator.root.findall('.//nfe:det', generator.ns)
    c.setFont("Helvetica", 7)
    iy = y - 12*mm
    for item in items[:15]:
        p = item.find('nfe:prod', generator.ns)
        cod = p.find('nfe:cProd', generator.ns).text if p.find('nfe:cProd', generator.ns) is not None else ''
        desc = p.find('nfe:xProd', generator.ns).text if p.find('nfe:xProd', generator.ns) is not None else ''
        ncm = p.find('nfe:NCM', generator.ns).text if p.find('nfe:NCM', generator.ns) is not None else ''
        qtd = float(p.find('nfe:qCom', generator.ns).text if p.find('nfe:qCom', generator.ns) is not None else 0)
        un = p.find('nfe:uCom', generator.ns).text if p.find('nfe:uCom', generator.ns) is not None else ''
        vun = float(p.find('nfe:vUnCom', generator.ns).text if p.find('nfe:vUnCom', generator.ns) is not None else 0)
        vtot = float(p.find('nfe:vProd', generator.ns).text if p.find('nfe:vProd', generator.ns) is not None else 0)
        
        c.drawString(m+2*mm, iy, cod[:10])
        c.drawString(m+20*mm, iy, desc[:45])
        c.drawString(m+90*mm, iy, ncm)
        c.drawRightString(m+127*mm, iy, f"{qtd:.3f}")
        c.drawString(m+130*mm, iy, un)
        c.drawRightString(m+165*mm, iy, f"{vun:.2f}")
        c.drawRightString(m+195*mm, iy, f"{vtot:.2f}")
        iy -= 5*mm
    
    # Info Adicional
    y -= ph + 2*mm
    ih = 20*mm
    c.rect(m, y-ih, w-2*m, ih)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m+2*mm, y-3*mm, "INFORMAÇÕES ADICIONAIS")
    inf = generator._get_text('.//nfe:infAdic/nfe:infCpl', '')
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-7*mm, inf[:100])
    
    c.save()

def gerar_v3(generator, output_path):
    """Layout NF-e 3.10 - Estruturado"""
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    m = 5*mm
    
    # Extração
    emit_nome = generator._get_text('.//nfe:emit/nfe:xNome')
    emit_cnpj = generator._format_cnpj(generator._get_text('.//nfe:emit/nfe:CNPJ'))
    emit_end = f"{generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xLgr')}, {generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:nro')}"
    emit_ie = generator._get_text('.//nfe:emit/nfe:IE')
    
    dest_nome = generator._get_text('.//nfe:dest/nfe:xNome')
    dest_doc = generator._get_text('.//nfe:dest/nfe:CNPJ') or generator._get_text('.//nfe:dest/nfe:CPF')
    dest_doc_fmt = generator._format_cnpj(dest_doc) if len(dest_doc) == 14 else generator._format_cpf(dest_doc)
    
    nf_num = generator._get_text('.//nfe:ide/nfe:nNF')
    nf_serie = generator._get_text('.//nfe:ide/nfe:serie')
    nf_tipo = generator._get_text('.//nfe:ide/nfe:tpNF')
    nf_data = generator._get_text('.//nfe:ide/nfe:dhEmi', generator._get_text('.//nfe:ide/nfe:dEmi'))
    chave = generator._get_text('.//nfe:protNFe/nfe:infProt/nfe:chNFe')
    
    if 'T' in nf_data:
        try:
            dt = datetime.fromisoformat(nf_data.replace('Z', '+00:00'))
            nf_data = dt.strftime('%d/%m/%Y')
        except:
            pass
    
    tot_bc = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vBC', '0'))
    tot_icms = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vICMS', '0'))
    tot_bc_st = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vBCST', '0'))
    tot_st = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vST', '0'))
    tot_prod = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vProd', '0'))
    tot_nf = float(generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vNF', '0'))
    
    y = h - m
    
    # Header
    hh = 30*mm
    c.rect(m, y-hh, 30*mm, hh)
    # c.drawCentredString(m+15*mm, y-hh/2, "LOGO")
    c.drawCentredString(m+15*mm, y-hh/2, "")
    
    c.rect(m+30*mm, y-hh, 90*mm, hh)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(m+35*mm, y-8*mm, "DANFE")
    c.setFont("Helvetica", 7)
    c.drawString(m+35*mm, y-12*mm, "DOCUMENTO AUXILIAR DA NF-e")
    c.drawString(m+35*mm, y-16*mm, f"0-ENTRADA / 1-SAÍDA: {nf_tipo}")
    c.drawString(m+35*mm, y-20*mm, f"Nº: {nf_num} - SÉRIE: {nf_serie} - FOLHA: 1/1")
    
    c.rect(m+120*mm, y-hh, 80*mm, hh)
    c.setFont("Helvetica", 6)
    # c.drawCentredString(m+160*mm, y-10*mm, "[CÓD BARRAS 44 DÍGITOS]")
    c.drawCentredString(m+160*mm, y-10*mm, "CHAVE DE ACESSO")
    c.setFont("Helvetica", 5)
    c.drawCentredString(m+160*mm, y-15*mm, generator._format_chave(chave))
    
    # Emitente
    y -= hh + 2*mm
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-6*mm, w-2*m, 6*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-4*mm, "EMITENTE")
    
    y -= 6*mm
    eh = 8*mm
    c.rect(m, y-eh, 140*mm, eh)
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-5*mm, f"NOME / RAZÃO SOCIAL: {emit_nome}")
    c.rect(m+140*mm, y-eh, 60*mm, eh)
    c.drawString(m+142*mm, y-5*mm, f"CNPJ: {emit_cnpj}")
    
    y -= eh
    c.rect(m, y-eh, 140*mm, eh)
    c.drawString(m+2*mm, y-5*mm, f"ENDEREÇO: {emit_end}")
    c.rect(m+140*mm, y-eh, 60*mm, eh)
    c.drawString(m+142*mm, y-5*mm, f"I.E.: {emit_ie}")
    
    # Destinatário
    y -= eh + 2*mm
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-6*mm, w-2*m, 6*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-4*mm, "DESTINATÁRIO / REMETENTE")
    
    y -= 6*mm
    dh = 8*mm
    c.rect(m, y-dh, 100*mm, dh)
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-5*mm, f"NOME: {dest_nome}")
    c.rect(m+100*mm, y-dh, 60*mm, dh)
    c.drawString(m+102*mm, y-5*mm, f"CNPJ/CPF: {dest_doc_fmt}")
    c.rect(m+160*mm, y-dh, 40*mm, dh)
    c.drawString(m+162*mm, y-5*mm, f"DATA: {nf_data}")
    
    # Cálculo Imposto
    y -= dh + 2*mm
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-6*mm, w-2*m, 6*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-4*mm, "CÁLCULO DO IMPOSTO")
    
    y -= 6*mm
    ch = 6*mm
    cw = (w-2*m) / 6
    
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-ch, w-2*m, ch, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 6)
    c.drawCentredString(m+cw*0.5, y-4*mm, "Base ICMS")
    c.drawCentredString(m+cw*1.5, y-4*mm, "Valor ICMS")
    c.drawCentredString(m+cw*2.5, y-4*mm, "Base ICMS ST")
    c.drawCentredString(m+cw*3.5, y-4*mm, "Valor ICMS ST")
    c.drawCentredString(m+cw*4.5, y-4*mm, "Tot Prod")
    c.drawCentredString(m+cw*5.5, y-4*mm, "Tot Nota")
    
    y -= ch
    c.rect(m, y-ch, w-2*m, ch)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(m+cw*0.5, y-4*mm, f"{tot_bc:.2f}")
    c.drawCentredString(m+cw*1.5, y-4*mm, f"{tot_icms:.2f}")
    c.drawCentredString(m+cw*2.5, y-4*mm, f"{tot_bc_st:.2f}")
    c.drawCentredString(m+cw*3.5, y-4*mm, f"{tot_st:.2f}")
    c.drawCentredString(m+cw*4.5, y-4*mm, f"{tot_prod:.2f}")
    c.drawCentredString(m+cw*5.5, y-4*mm, f"{tot_nf:.2f}")
    
    # Produtos
    y -= ch + 2*mm
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-6*mm, w-2*m, 6*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-4*mm, "DADOS DO PRODUTO/SERVIÇO")
    
    y -= 6*mm
    rh = 5*mm
    
    c.setFillColor(colors.lightgrey)
    c.rect(m, y-rh, w-2*m, rh, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(m+2*mm, y-3.5*mm, "Cód")
    c.drawString(m+22*mm, y-3.5*mm, "Descrição")
    c.drawString(m+105*mm, y-3.5*mm, "NCM")
    c.drawString(m+125*mm, y-3.5*mm, "Qtd")
    c.drawString(m+150*mm, y-3.5*mm, "V.Unit")
    c.drawString(m+175*mm, y-3.5*mm, "V.Total")
    
    y -= rh
    items = generator.root.findall('.//nfe:det', generator.ns)
    c.setFont("Helvetica", 7)
    
    for item in items[:12]:
        p = item.find('nfe:prod', generator.ns)
        cod = p.find('nfe:cProd', generator.ns).text if p.find('nfe:cProd', generator.ns) is not None else ''
        desc = p.find('nfe:xProd', generator.ns).text if p.find('nfe:xProd', generator.ns) is not None else ''
        ncm = p.find('nfe:NCM', generator.ns).text if p.find('nfe:NCM', generator.ns) is not None else ''
        qtd = float(p.find('nfe:qCom', generator.ns).text if p.find('nfe:qCom', generator.ns) is not None else 0)
        vun = float(p.find('nfe:vUnCom', generator.ns).text if p.find('nfe:vUnCom', generator.ns) is not None else 0)
        vtot = float(p.find('nfe:vProd', generator.ns).text if p.find('nfe:vProd', generator.ns) is not None else 0)
        
        c.rect(m, y-rh, w-2*m, rh)
        c.drawString(m+2*mm, y-3.5*mm, cod[:10])
        c.drawString(m+22*mm, y-3.5*mm, desc[:50])
        c.drawString(m+105*mm, y-3.5*mm, ncm)
        c.drawRightString(m+145*mm, y-3.5*mm, f"{qtd:.3f}")
        c.drawRightString(m+170*mm, y-3.5*mm, f"{vun:.2f}")
        c.drawRightString(m+195*mm, y-3.5*mm, f"{vtot:.2f}")
        y -= rh
    
    # Info Adicional
    y -= 2*mm
    ih = 25*mm
    c.rect(m, y-ih, w-2*m, ih)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m+2*mm, y-3*mm, "DADOS ADICIONAIS")
    inf = generator._get_text('.//nfe:infAdic/nfe:infCpl', '')
    c.setFont("Helvetica", 7)
    c.drawString(m+2*mm, y-7*mm, inf[:120])
    
    c.save()

def gerar_v4(generator, output_path):
    """Gera o DANFE em PDF seguindo o layout do protótipo"""
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 5*mm
    
    # ========== EXTRAÇÃO DE DADOS ==========
    # Emitente
    emit_cnpj = generator._get_text('.//nfe:emit/nfe:CNPJ')
    emit_nome = generator._get_text('.//nfe:emit/nfe:xNome')
    emit_fantasia = generator._get_text('.//nfe:emit/nfe:xFant')
    emit_logradouro = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xLgr')
    emit_numero = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:nro')
    emit_bairro = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xBairro')
    emit_municipio = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:xMun')
    emit_uf = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:UF')
    emit_cep = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:CEP')
    emit_fone = generator._get_text('.//nfe:emit/nfe:enderEmit/nfe:fone')
    emit_ie = generator._get_text('.//nfe:emit/nfe:IE')
    
    # Destinatário
    dest_cnpj = generator._get_text('.//nfe:dest/nfe:CNPJ')
    dest_cpf = generator._get_text('.//nfe:dest/nfe:CPF')
    dest_nome = generator._get_text('.//nfe:dest/nfe:xNome')
    dest_logradouro = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:xLgr')
    dest_numero = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:nro')
    dest_bairro = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:xBairro')
    dest_municipio = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:xMun')
    dest_uf = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:UF')
    dest_cep = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:CEP')
    dest_fone = generator._get_text('.//nfe:dest/nfe:enderDest/nfe:fone')
    dest_ie = generator._get_text('.//nfe:dest/nfe:IE', 'ISENTO')
    
    # Nota Fiscal
    nf_numero = generator._get_text('.//nfe:ide/nfe:nNF')
    nf_serie = generator._get_text('.//nfe:ide/nfe:serie')
    nf_data_emissao = generator._get_text('.//nfe:ide/nfe:dhEmi')
    nf_tipo = generator._get_text('.//nfe:ide/nfe:tpNF')
    nf_natureza = generator._get_text('.//nfe:ide/nfe:natOp')
    nf_protocolo = generator._get_text('.//nfe:protNFe/nfe:infProt/nfe:nProt')
    nf_chave = generator._get_text('.//nfe:protNFe/nfe:infProt/nfe:chNFe')
    
    # Totais
    total_bc_icms = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vBC', '0.00')
    total_icms = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vICMS', '0.00')
    total_bc_st = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vBCST', '0.00')
    total_st = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vST', '0.00')
    total_produtos = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vProd', '0.00')
    total_frete = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vFrete', '0.00')
    total_seguro = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vSeg', '0.00')
    total_desconto = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vDesc', '0.00')
    total_ipi = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vIPI', '0.00')
    total_nf = generator._get_text('.//nfe:total/nfe:ICMSTot/nfe:vNF', '0.00')
    
    # Transportadora
    transp_nome = generator._get_text('.//nfe:transp/nfe:transporta/nfe:xNome', '')
    transp_placa = generator._get_text('.//nfe:transp/nfe:veicTransp/nfe:placa', '')
    transp_mod_frete = generator._get_text('.//nfe:transp/nfe:modFrete', '9')
    
    # Formata datas
    data_emissao_fmt = ''
    hora_emissao_fmt = ''
    if nf_data_emissao:
        try:
            dt = datetime.fromisoformat(nf_data_emissao.replace('Z', '+00:00'))
            data_emissao_fmt = dt.strftime('%d/%m/%Y')
            hora_emissao_fmt = dt.strftime('%H:%M:%S')
        except:
            data_emissao_fmt = nf_data_emissao
    
    # ========== INÍCIO DO LAYOUT ==========
    y = height - margin
    
    # ========== CABEÇALHO: LOGOMARCA | DANFE | CHAVE ==========
    header_height = 35*mm
    col1_width = 60*mm  # Logomarca
    col2_width = 80*mm  # DANFE
    col3_width = 60*mm  # Chave
    
    # Coluna 1: Logomarca (placeholder)
    c.rect(margin, y - header_height, col1_width, header_height)
    c.setFont("Helvetica", 10)
    # c.drawCentredString(margin + col1_width/2, y - header_height/2, "[LOGOMARCA]")
    c.drawCentredString(margin + col1_width/2, y - header_height/2, "")
    
    # Coluna 2: DANFE
    col2_x = margin + col1_width
    c.rect(col2_x, y - header_height, col2_width, header_height)
    
    # Título DANFE
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(col2_x + col2_width/2, y - 8*mm, "DANFE")
    c.setFont("Helvetica", 7)
    c.drawCentredString(col2_x + col2_width/2, y - 12*mm, "DOCUMENTO AUXILIAR DA NOTA FISCAL ELETRÔNICA")
    
    # Linha separadora
    c.line(col2_x, y - 14*mm, col2_x + col2_width, y - 14*mm)
    
    # Tipo de operação
    tipo_operacao = "0 - Entrada" if nf_tipo == "0" else "1 - Saída"
    c.setFont("Helvetica", 8)
    c.drawCentredString(col2_x + col2_width/2, y - 18*mm, tipo_operacao + ": ")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x + col2_width/2 + 10*mm, y - 18*mm, nf_tipo)
    
    # Linha separadora
    c.line(col2_x, y - 20*mm, col2_x + col2_width, y - 20*mm)
    
    # Número e Série
    c.setFont("Helvetica", 8)
    numero_formatado = f"{int(nf_numero):09d}" if nf_numero else "000000000"
    c.drawCentredString(col2_x + col2_width/2, y - 25*mm, f"Nº {numero_formatado} - SÉRIE {nf_serie}")
    c.setFont("Helvetica", 7)
    c.drawCentredString(col2_x + col2_width/2, y - 29*mm, "FOLHA 1/1")
    
    # Coluna 3: Chave de Acesso
    col3_x = col2_x + col2_width
    c.rect(col3_x, y - header_height, col3_width, header_height)
    
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(col3_x + col3_width/2, y - 4*mm, "CHAVE DE ACESSO")
    
    c.setFont("Helvetica", 6.5)
    chave_formatada = generator._format_chave(nf_chave)
    # Quebra a chave em 3 linhas
    chave_parts = chave_formatada.split()
    linha1 = ' '.join(chave_parts[0:4])
    linha2 = ' '.join(chave_parts[4:8])
    linha3 = ' '.join(chave_parts[8:11])
    
    c.drawCentredString(col3_x + col3_width/2, y - 8*mm, linha1)
    c.drawCentredString(col3_x + col3_width/2, y - 11*mm, linha2)
    c.drawCentredString(col3_x + col3_width/2, y - 14*mm, linha3)
    
    # Código de barras (placeholder)
    c.setFillColor(colors.lightgrey)
    c.rect(col3_x + 5*mm, y - 30*mm, col3_width - 10*mm, 14*mm, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 6)
    # c.drawCentredString(col3_x + col3_width/2, y - 23*mm, "[CÓDIGO DE BARRAS]")
    
    # ========== DADOS DO EMITENTE ==========
    y -= header_height + 2*mm
    box_height = 8*mm
    
    generator._draw_box(c, margin, y - box_height, 100*mm, box_height,
                    "Nome / Razão Social", emit_nome, 9)
    
    generator._draw_box(c, margin + 100*mm, y - box_height, 55*mm, box_height,
                    "CNPJ", generator._format_cnpj(emit_cnpj), 9)
    
    generator._draw_box(c, margin + 155*mm, y - box_height, 45*mm, box_height,
                    "IE", emit_ie, 9)
    
    # ========== DADOS DO DESTINATÁRIO ==========
    y -= box_height + 2*mm
    
    cnpj_cpf = dest_cnpj if dest_cnpj else dest_cpf
    cnpj_cpf_label = "CNPJ" if len(cnpj_cpf) == 14 else "CPF"
    cnpj_cpf_formatado = generator._format_cnpj(cnpj_cpf) if len(cnpj_cpf) == 14 else generator._format_cpf(cnpj_cpf)
    
    generator._draw_box(c, margin, y - box_height, 100*mm, box_height,
                    "Nome / Razão Social", dest_nome, 9, False)
    
    generator._draw_box(c, margin + 100*mm, y - box_height, 60*mm, box_height,
                    cnpj_cpf_label, cnpj_cpf_formatado, 9, False)
    
    generator._draw_box(c, margin + 160*mm, y - box_height, 40*mm, box_height,
                    "Data Emissão", data_emissao_fmt, 9, False)
    
    # Linha 2
    y -= box_height
    
    generator._draw_box(c, margin, y - box_height, 100*mm, box_height,
                    "Endereço", f"{dest_logradouro}, {dest_numero}", 8, False)
    
    generator._draw_box(c, margin + 100*mm, y - box_height, 60*mm, box_height,
                    "Bairro", dest_bairro, 8, False)
    
    generator._draw_box(c, margin + 160*mm, y - box_height, 40*mm, box_height,
                    "CEP", generator._format_cep(dest_cep), 8, False)
    
    # Linha 3
    y -= box_height
    
    generator._draw_box(c, margin, y - box_height, 80*mm, box_height,
                    "Município", dest_municipio, 8, False)
    
    generator._draw_box(c, margin + 80*mm, y - box_height, 80*mm, box_height,
                    "UF/IE", f"{dest_uf} / {dest_ie}", 8, False)
    
    generator._draw_box(c, margin + 160*mm, y - box_height, 40*mm, box_height,
                    "Hora Emissão", hora_emissao_fmt, 8, False)
    
    # ========== FATURA (se houver) ==========
    y -= box_height + 2*mm
    fatura_height = 8*mm
    
    c.rect(margin, y - fatura_height, width - 2*margin, fatura_height)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin + 2*mm, y - 3*mm, "FATURA/DUPLICATA")
    c.setFont("Helvetica", 8)
    # Aqui você pode adicionar dados de duplicatas se houver no XML
    c.drawString(margin + 2*mm, y - 6*mm, f"Nº {nf_numero} - {data_emissao_fmt} - R$ {float(total_nf):.2f}")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - margin - 2*mm, y - 5*mm, f"Valor Total: R$ {float(total_nf):.2f}")
    
    # ========== PRODUTOS ==========
    y -= fatura_height + 2*mm
    
    # Cabeçalho da tabela
    row_height = 6*mm
    c.setFillColor(colors.lightgrey)
    c.rect(margin, y - row_height, width - 2*margin, row_height, fill=1)
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica-Bold", 6.5)
    
    # Definir colunas
    cols_x = [
        margin + 2*mm,      # Código
        margin + 20*mm,     # Descrição
        margin + 90*mm,     # NCM
        margin + 105*mm,    # CST
        margin + 118*mm,    # CFOP
        margin + 130*mm,    # Un
        margin + 140*mm,    # Qtd
        margin + 155*mm,    # V.Unit
        margin + 175*mm     # V.Prod
    ]
    
    c.drawString(cols_x[0], y - 3.5*mm, "Cód.")
    c.drawString(cols_x[1], y - 3.5*mm, "Descrição")
    c.drawString(cols_x[2], y - 3.5*mm, "NCM")
    c.drawString(cols_x[3], y - 3.5*mm, "CST")
    c.drawString(cols_x[4], y - 3.5*mm, "CFOP")
    c.drawString(cols_x[5], y - 3.5*mm, "Un.")
    c.drawString(cols_x[6], y - 3.5*mm, "Qtd.")
    c.drawString(cols_x[7], y - 3.5*mm, "V.Unit")
    c.drawString(cols_x[8], y - 3.5*mm, "V.Prod")
    
    # Produtos
    y -= row_height
    items = generator.root.findall('.//nfe:det', generator.ns)
    c.setFont("Helvetica", 7)
    
    max_items = 12
    for idx, item in enumerate(items[:max_items]):
        prod = item.find('nfe:prod', generator.ns)
        imposto = item.find('nfe:imposto', generator.ns)
        
        codigo = prod.find('nfe:cProd', generator.ns).text if prod.find('nfe:cProd', generator.ns) is not None else ''
        descricao = prod.find('nfe:xProd', generator.ns).text if prod.find('nfe:xProd', generator.ns) is not None else ''
        ncm = prod.find('nfe:NCM', generator.ns).text if prod.find('nfe:NCM', generator.ns) is not None else ''
        cfop = prod.find('nfe:CFOP', generator.ns).text if prod.find('nfe:CFOP', generator.ns) is not None else ''
        unid = prod.find('nfe:uCom', generator.ns).text if prod.find('nfe:uCom', generator.ns) is not None else ''
        qtd = prod.find('nfe:qCom', generator.ns).text if prod.find('nfe:qCom', generator.ns) is not None else '0'
        vlr_unit = prod.find('nfe:vUnCom', generator.ns).text if prod.find('nfe:vUnCom', generator.ns) is not None else '0.00'
        vlr_total = prod.find('nfe:vProd', generator.ns).text if prod.find('nfe:vProd', generator.ns) is not None else '0.00'
        
        # ICMS
        icms = imposto.find('.//nfe:ICMS', generator.ns) if imposto is not None else None
        cst = ''
        if icms is not None:
            for icms_child in icms:
                cst_elem = icms_child.find('nfe:CST', generator.ns)
                if cst_elem is None:
                    cst_elem = icms_child.find('nfe:CSOSN', generator.ns)
                if cst_elem is not None:
                    cst = cst_elem.text
                    break
        
        # Desenha linha
        c.rect(margin, y - row_height, width - 2*margin, row_height)
        
        c.drawString(cols_x[0], y - 4*mm, codigo[:8])
        c.drawString(cols_x[1], y - 4*mm, descricao[:45])
        c.drawString(cols_x[2], y - 4*mm, ncm)
        c.drawString(cols_x[3], y - 4*mm, cst)
        c.drawString(cols_x[4], y - 4*mm, cfop)
        c.drawString(cols_x[5], y - 4*mm, unid)
        c.drawRightString(cols_x[6] + 12*mm, y - 4*mm, f"{float(qtd):.2f}")
        c.drawRightString(cols_x[7] + 18*mm, y - 4*mm, f"{float(vlr_unit):.2f}")
        c.drawRightString(cols_x[8] + 23*mm, y - 4*mm, f"{float(vlr_total):.2f}")
        
        y -= row_height
    
    # ========== TOTAIS ==========
    y -= 2*mm
    totais_height = 8*mm
    
    c.rect(margin, y - totais_height, width - 2*margin, totais_height)
    c.setFont("Helvetica", 7)
    
    tot_width = (width - 2*margin) / 5
    c.drawString(margin + 2*mm, y - 3*mm, f"Base ICMS: {float(total_bc_icms):.2f}")
    c.drawString(margin + tot_width + 2*mm, y - 3*mm, f"Valor ICMS: {float(total_icms):.2f}")
    c.drawString(margin + 2*tot_width + 2*mm, y - 3*mm, f"Base ICMS ST: {float(total_bc_st):.2f}")
    c.drawString(margin + 3*tot_width + 2*mm, y - 3*mm, f"Valor ICMS ST: {float(total_st):.2f}")
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 4*tot_width + 2*mm, y - 5*mm, f"Valor Tot: {float(total_nf):.2f}")
    
    # ========== TRANSPORTADOR ==========
    y -= totais_height + 2*mm
    transp_height = 8*mm
    
    frete_desc = {
        '0': '0 - CIF',
        '1': '1 - FOB',
        '2': '2 - Por conta terceiros',
        '3': '3 - Próprio remetente',
        '4': '4 - Próprio destinatário',
        '9': '9 - Sem frete'
    }
    
    c.rect(margin, y - transp_height, width - 2*margin, transp_height)
    c.setFont("Helvetica", 7)
    c.drawString(margin + 2*mm, y - 3*mm, f"Frete: {frete_desc.get(transp_mod_frete, '9 - Sem frete')}")
    c.drawString(margin + 2*mm, y - 6*mm, f"Transportador: {transp_nome}")
    c.drawString(margin + 100*mm, y - 6*mm, f"Placa: {transp_placa}")
    
    # ========== INFORMAÇÕES COMPLEMENTARES ==========
    y -= transp_height + 2*mm
    info_height = 25*mm
    
    inf_complementar = generator._get_text('.//nfe:infAdic/nfe:infCpl', '')
    protocolo_texto = f"Protocolo Autorização: {nf_protocolo} - {data_emissao_fmt} {hora_emissao_fmt}" if nf_protocolo else ""
    
    c.rect(margin, y - info_height, width - 2*margin, info_height)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin + 2*mm, y - 3*mm, "INFORMAÇÕES COMPLEMENTARES")
    
    c.setFont("Helvetica", 7)
    y_text = y - 7*mm
    
    if inf_complementar:
        # Quebra texto em linhas
        max_chars = 120
        palavras = inf_complementar.split()
        linha_atual = ""
        for palavra in palavras:
            if len(linha_atual) + len(palavra) + 1 <= max_chars:
                linha_atual += palavra + " "
            else:
                c.drawString(margin + 2*mm, y_text, linha_atual)
                y_text -= 3*mm
                linha_atual = palavra + " "
        if linha_atual:
            c.drawString(margin + 2*mm, y_text, linha_atual)
            y_text -= 3*mm
    
    if protocolo_texto:
        c.drawString(margin + 2*mm, y_text, protocolo_texto)
    
    c.save()