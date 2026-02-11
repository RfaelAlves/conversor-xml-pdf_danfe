import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os
import glob
from pathlib import Path

class DANFEGenerator:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        self.ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        self.versao = self._detectar_versao()
        
    def _detectar_versao(self):
        """Detecta automaticamente a versão do XML"""
        inf_nfe = self.root.find('.//nfe:infNFe', self.ns)
        if inf_nfe is not None:
            versao = inf_nfe.get('versao', '')
            if versao.startswith('4.'):
                return '4.00'
            elif versao.startswith('3.'):
                return '3.10'
            elif versao.startswith('2.'):
                return '2.00'
        
        # Detecta pela estrutura
        ide = self.root.find('.//nfe:ide', self.ns)
        if ide is not None:
            if ide.find('nfe:indFinal', self.ns) is not None:
                return '4.00'
            elif ide.find('nfe:idDest', self.ns) is not None:
                return '3.10'
        return '2.00'
    
    def _get_text(self, path, default=''):
        element = self.root.find(path, self.ns)
        return element.text if element is not None else default
    
    def _format_cnpj(self, cnpj):
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
    
    def _format_cpf(self, cpf):
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    def _format_cep(self, cep):
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
    
    def _format_chave(self, chave):
        if len(chave) == 44:
            return ' '.join([chave[i:i+4] for i in range(0, 44, 4)])
        return chave
    
    def _sanitize_filename(self, filename):
        for char in '<>:"/\\|?*':
            filename = filename.replace(char, '')
        return filename.strip()
    
    def _draw_box(self, c, x, y, width, height, label, value, font_size=9, value_bold=True):
        c.rect(x, y, width, height)
        c.setFont("Helvetica-Bold", 6)
        c.drawString(x + 1*mm, y + height - 2.5*mm, label.upper())
        c.setFont("Helvetica-Bold" if value_bold else "Helvetica", font_size)
        c.drawString(x + 1*mm, y + height - 6*mm, str(value))
    
    def get_output_filename(self):
        nf_numero = self._get_text('.//nfe:ide/nfe:nNF', 'SEM_NUMERO')
        dest_nome = self._get_text('.//nfe:dest/nfe:xNome', 'DEST_DESCONHECIDO')
        dest_nome_limpo = self._sanitize_filename(dest_nome)
        return f"{nf_numero} - {dest_nome_limpo}.pdf"
    
    def generate_danfe(self, output_path):
        """Gera DANFE de acordo com a versão"""
        print(f"Gerando DANFE versão {self.versao}: {os.path.basename(output_path)}")
        
        if self.versao == '2.00':
            from danfe_layouts import gerar_v2
            gerar_v2(self, output_path)
        elif self.versao == '3.10':
            from danfe_layouts import gerar_v3
            gerar_v3(self, output_path)
        else:
            from danfe_layouts import gerar_v4
            gerar_v4(self, output_path)

def processar_pasta(pasta_entrada, pasta_saida=None, mostrar_progresso=True):
    """Processa todos os XMLs em uma pasta"""
    if pasta_saida is None:
        pasta_saida = pasta_entrada
    
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    arquivos_xml = glob.glob(os.path.join(pasta_entrada, "*.xml"))
    total = len(arquivos_xml)
    
    print(f"Encontrados {total} arquivos XML")
    print(f"Pasta saída: {pasta_saida}")
    print("-" * 80)
    
    sucesso = erros = 0
    arquivos_com_erro = []
    
    for i, xml_path in enumerate(arquivos_xml, 1):
        try:
            generator = DANFEGenerator(xml_path)
            nome_pdf = generator.get_output_filename()
            output_path = os.path.join(pasta_saida, nome_pdf)
            generator.generate_danfe(output_path)
            sucesso += 1
            
            if mostrar_progresso and i % 100 == 0:
                print(f"Progresso: {i}/{total} ({i/total*100:.1f}%) - Sucessos: {sucesso} | Erros: {erros}")
        
        except Exception as e:
            erros += 1
            arquivos_com_erro.append((os.path.basename(xml_path), str(e)))
            if mostrar_progresso and erros % 50 == 0:
                print(f"AVISO: {erros} erros até agora")
    
    print("\n" + "=" * 80)
    print(f"CONCLUÍDO - Sucessos: {sucesso} | Erros: {erros} | Taxa: {sucesso/total*100:.2f}%")
    
    if arquivos_com_erro:
        # Salva log em arquivo
        log_path = os.path.join(pasta_saida, "log_erros.txt")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("ARQUIVOS COM ERRO\n" + "=" * 80 + "\n\n")
            for arq, erro in arquivos_com_erro:
                f.write(f"Arquivo: {arq}\nErro: {erro}\n" + "-" * 80 + "\n")
        print(f"Log salvo em: {log_path}")
        
        # Exibe lista de erros no console
        print("\n" + "=" * 80)
        print("LISTA DE ARQUIVOS COM ERRO:")
        print("=" * 80)
        for i, (arq, erro) in enumerate(arquivos_com_erro, 1):
            print(f"\n[{i}] Arquivo: {arq}")
            print(f"    Erro: {erro}")
        print("=" * 80)
    
    return sucesso, erros

if __name__ == "__main__":
    pasta_xml = f"{Path.cwd()}\\xml"
    pasta_pdf = f"{Path.cwd()}\\xml\\pdf"
    
    processar_pasta(pasta_xml, pasta_pdf)