from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image

from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone

# ---------- SEÇÃO HERO (Singleton) ----------
class SecaoHero(models.Model):
    titulo = models.CharField(max_length=100, default="LIGHT WORK")
    subtitulo = models.CharField(max_length=200, default="Formando Profissionais para o Mercado de Trabalho")
    descricao = models.TextField(
        default="Cursos Técnicos de Informática, Contabilidade, Eletricidade, "
                "Refrigeração e Climatização, e muito mais. Capacitação de excelência com foco em empregabilidade."
    )
    preco = models.FloatField(default=800.0)
    rotulo_preco = models.CharField(max_length=50, default="Cada curso")
    info_parcelamento = models.CharField(max_length=100, default="parcelamento disponível")
    texto_botao_primario = models.CharField(max_length=50, default="Matricular Agora")
    link_botao_primario = models.CharField(max_length=255, default="{% url 'matricula' %}")
    texto_botao_secundario = models.CharField(max_length=50, default="Conhecer Cursos")
    link_botao_secundario = models.CharField(max_length=200, default="#cursos")

    class Meta:
        verbose_name = "Seção Hero"
        verbose_name_plural = "Seções Hero"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class ImagemCarrossel(models.Model):
    secao_hero = models.ForeignKey(
        'SecaoHero',
        on_delete=models.CASCADE,
        related_name='imagens_carrossel'
    )
    # Campo de imagem com upload automático
    imagem = models.ImageField(
        upload_to='carrossel/%Y/%m/',  # Ex: carrossel/2026/06/
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        max_length=255,
        help_text="Formatos permitidos: JPG, JPEG, PNG, GIF, WEBP"
    )
    alt = models.CharField(max_length=255, verbose_name="Texto alternativo")
    ativo = models.BooleanField(default=False, verbose_name="Ativo no carrossel")

    class Meta:
        verbose_name = "Imagem do Carrossel"
        verbose_name_plural = "Imagens do Carrossel"
        ordering = ['-ativo', 'id']  # Ativos primeiro

    def __str__(self):
        return self.alt or "Imagem sem descrição"

    # (Opcional) Redimensionar imagem ao salvar
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva o arquivo primeiro

        # Redimensiona se a largura for maior que 1200px
        if self.imagem:
            try:
                img = Image.open(self.imagem.path)
                if img.width > 1200:
                    nova_largura = 1200
                    nova_altura = int(img.height * (nova_largura / img.width))
                    img = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
                    img.save(self.imagem.path)
            except Exception as e:
                # Log do erro (pode usar logging)
                print(f"Erro ao redimensionar imagem: {e}")

    # (Opcional) Propriedade para manter compatibilidade com código antigo que usava 'src'
    @property
    def src(self):
        """Retorna a URL da imagem para compatibilidade."""
        return self.imagem.url if self.imagem else ''


# ---------- SEÇÃO ESTATÍSTICAS (Singleton) ----------
class SecaoEstatisticas(models.Model):
    class Meta:
        verbose_name = "Seção Estatísticas"
        verbose_name_plural = "Seções Estatísticas"

    def __str__(self):
        return "Estatísticas"

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class ItemEstatistica(models.Model):
    secao_estatisticas = models.ForeignKey(SecaoEstatisticas, on_delete=models.CASCADE, related_name='itens')
    numero = models.CharField(max_length=20)  # "+2.000"
    rotulo = models.CharField(max_length=100)  # "Alunos Formados"
    descricao = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "Item Estatístico"
        verbose_name_plural = "Itens Estatísticos"

    def __str__(self):
        return f"{self.numero} - {self.rotulo}"


# ---------- SEÇÃO CURSOS (Singleton) ----------
class SecaoCursos(models.Model):
    titulo = models.CharField(max_length=100, default="Nossos Cursos Técnicos")
    subtitulo = models.CharField(max_length=200, default="Formação completa e atualizada, com forte ligação ao mercado de trabalho.")
    texto_chamada = models.CharField(max_length=100, default="Garanta a sua vaga")
    link_chamada = models.CharField(max_length=200, default="index2.html#matriculas")

    class Meta:
        verbose_name = "Seção Cursos"
        verbose_name_plural = "Seções Cursos"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class Curso(models.Model):
    secao_cursos = models.ForeignKey(SecaoCursos, on_delete=models.CASCADE, related_name='cursos')
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50)  # "fa-bolt"
    descricao = models.TextField()
    imagem = models.ImageField(max_length=255)  # caminho da imagem
    duracao = models.CharField(max_length=50)  # "2 meses (72 horas)"
    pre_requisitos = models.CharField(max_length=200)  # "Ensino básico completo (9ª classe)"
    preco = models.CharField(max_length=20)  # "800 MZN"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome


#=============================================================================

class Matricula(models.Model):
    # Dados pessoais
    nome_completo = models.CharField('Nome completo', max_length=200)
    data_nascimento = models.DateField('Data de nascimento')
    genero = models.CharField(
        'Gênero',
        max_length=20,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('O', 'Outro'),
        ]
    )
    nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Moçambicana')
    bilhete_identidade = models.CharField(
        'BI/NUIT',
        max_length=30,
        validators=[MinLengthValidator(8)],
        unique=True
    )

    # Contacto
    telefone = models.CharField(
        'Telefone',
        max_length=20,
        validators=[RegexValidator(r'^\+?258?[0-9]{9,12}$', 'Número inválido')]
    )
    email = models.EmailField('E-mail', blank=True)
    endereco = models.TextField('Endereço', max_length=300)

    # Curso pretendido
    curso = models.ForeignKey(
        'Curso',
        on_delete=models.PROTECT,
        verbose_name='Curso pretendido',
        related_name='matriculas'
    )

    # Opções de pagamento
    FORMA_PAGAMENTO_CHOICES = [
        ('V', 'À vista'),
        ('P', 'Parcelado (3x)'),
    ]
    forma_pagamento = models.CharField(
        'Forma de pagamento',
        max_length=1,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='V', blank=True,
    )

    # Observações
    observacoes = models.TextField('Observações', blank=True)

    # Status da matrícula
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Confirmada'),
        ('A', 'Aprovada'),
        ('R', 'Rejeitada'),
        ('M', 'Matriculado'),
    ]
    status = models.CharField(
        'Status',
        max_length=1,
        choices=STATUS_CHOICES,
        default='P', blank=True,
    )

    # Datas
    data_criacao = models.DateTimeField('Data de inscrição', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última atualização', auto_now=True)

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'{self.nome_completo} - {self.curso.nome}'

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Desconhecido')


# ---------- SEÇÃO SOBRE (Singleton) ----------
class SecaoSobre(models.Model):
    texto_distintivo = models.CharField(max_length=100, default="+1 mês de história")
    titulo = models.CharField(max_length=100, default="Quem Somos")
    missao = models.TextField(
        default="Capacitar profissionais com excelência técnica, ética e visão "
                "empreendedora, conectando-os ao mercado de trabalho."
    )
    visao = models.TextField(
        default="Ser referência nacional em educação profissional técnica, "
                "reconhecida pela inovação e empregabilidade dos seus egressos."
    )
    valores = models.TextField(default="Inovação, compromisso social, rigor técnico e parceria com a indústria.")
    historia = models.TextField(
        default="Fundado em 2026, o Instituto Educativo já formou mais de 10 profissionais "
                "que atuam nas maiores empresas da região. Nossa metodologia combina "
                "teoria atualizada com prática intensiva em laboratórios."
    )
    # MUDANÇA AQUI: de CharField para ImageField
    imagem = models.ImageField(
        upload_to='sobre/%Y/%m/',  # ex: sobre/2026/06/
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        max_length=255,
        blank=True,
        null=True,
        help_text="Formatos permitidos: JPG, JPEG, PNG, GIF, WEBP"
    )

    class Meta:
        verbose_name = "Seção Sobre"
        verbose_name_plural = "Seções Sobre"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    # (Opcional) Redimensionar imagem ao salvar
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva o arquivo primeiro

        # Redimensiona se a largura for maior que 1200px
        if self.imagem:
            try:
                img = Image.open(self.imagem.path)
                if img.width > 1200:
                    nova_largura = 1200
                    nova_altura = int(img.height * (nova_largura / img.width))
                    img = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
                    img.save(self.imagem.path)
            except Exception as e:
                # Log do erro (pode usar logging)
                print(f"Erro ao redimensionar imagem: {e}")

    # Propriedade para compatibilidade com templates que usam 'url_imagem'
    @property
    def url_imagem(self):
        """Retorna a URL da imagem para compatibilidade com o template antigo."""
        return self.imagem.url if self.imagem else ''


# ---------- SEÇÃO INFRAESTRUTURA (Singleton) ----------
class SecaoInfraestrutura(models.Model):
    titulo = models.CharField(max_length=100, default="Infraestrutura de Ponta")
    subtitulo = models.CharField(max_length=200, default="Ambientes preparados para o aprendizado prático e desenvolvimento profissional")

    class Meta:
        verbose_name = "Seção Infraestrutura"
        verbose_name_plural = "Seções Infraestrutura"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class ItemInfraestrutura(models.Model):
    secao_infraestrutura = models.ForeignKey(SecaoInfraestrutura, on_delete=models.CASCADE, related_name='itens')
    icone = models.CharField(max_length=50)  # "fa-microscope"
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Item de Infraestrutura"
        verbose_name_plural = "Itens de Infraestrutura"

    def __str__(self):
        return self.titulo


# ---------- SEÇÃO DEPOIMENTOS (Singleton) ----------
class SecaoDepoimentos(models.Model):
    titulo = models.CharField(max_length=100, default="O que dizem os nossos alunos")
    subtitulo = models.CharField(max_length=200, default="Depoimentos reais de quem já conquistou seu espaço no mercado")

    class Meta:
        verbose_name = "Seção Depoimentos"
        verbose_name_plural = "Seções Depoimentos"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class Depoimento(models.Model):
    secao_depoimentos = models.ForeignKey(SecaoDepoimentos, on_delete=models.CASCADE, related_name='depoimentos')
    citacao = models.TextField()
    autor_nome = models.CharField(max_length=100)
    autor_cargo = models.CharField(max_length=100)
    icone_avatar = models.CharField(max_length=50, default="fas fa-user-circle")  # ou URL

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"

    def __str__(self):
        return f"{self.autor_nome} - {self.autor_cargo[:30]}"


# ---------- SEÇÃO MATRÍCULAS (Singleton) ----------
class SecaoMatriculas(models.Model):
    titulo = models.CharField(max_length=100, default="As Matrículas para 2026 Estão Abertas")
    subtitulo = models.TextField(
        default="Garanta sua vaga e invista no futuro com cursos técnicos de alta "
                "empregabilidade. Condições especiais para matrícula antecipada."
    )
    texto_botao = models.CharField(max_length=50, default="Inscrever-se Agora")
    link_botao = models.CharField(max_length=200, default="#")

    class Meta:
        verbose_name = "Seção Matrículas"
        verbose_name_plural = "Seções Matrículas"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


# ---------- SEÇÃO CONTACTO (Singleton) ----------
class InformacaoContacto(models.Model):
    telefone = models.CharField(max_length=20, default="+258 87 250 1337")
    whatsapp = models.CharField(max_length=50, default="+258 84 560 1278 / +258 86 143 2429")
    email = models.EmailField(default="secretaria@instecnico.co.mz")
    endereco = models.CharField(max_length=200, default="Av. União Africana, Casa Branca, Matola")
    url_mapa_embed = models.TextField(
        default="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3588.0116271856295!2d32.502157!3d-25.934842999999997!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMjXCsDU2JzA1LjQiUyAzMsKwMzAnMDcuOCJF!5e0!3m2!1spt-PT!2smz!4v1781707179291!5m2!1spt-PT!2smz"
    )
    referencia_mapa = models.CharField(max_length=200, default="📍 Referência: Atrás das Bombas Total, na Papelaria Popular")

    class Meta:
        verbose_name = "Informação de Contacto"
        verbose_name_plural = "Informações de Contacto"

    def __str__(self):
        return "Contactos"

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


# ---------- SEÇÃO RODAPÉ (Singleton) ----------
class SecaoRodape(models.Model):
    nome_instituto = models.CharField(max_length=100, default="INSTITUTO EDUCATIVO")
    descricao = models.TextField(
        default="Instituto técnico referência em Maputo-Matola, formando profissionais com propósito e empregabilidade."
    )
    horario_funcionamento = models.TextField(default="Segunda a Sexta: 8h - 20h\nSábado: 9h - 13h")
    texto_copyright = models.CharField(max_length=200, default="© 2026 INSTITUTO EDUCATIVO. Todos os direitos reservados. Compromisso com a empregabilidade.")

    class Meta:
        verbose_name = "Seção Rodapé"
        verbose_name_plural = "Seções Rodapé"

    def __str__(self):
        return self.nome_instituto

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class LinkSocial(models.Model):
    secao_rodape = models.ForeignKey(SecaoRodape, on_delete=models.CASCADE, related_name='links_sociais')
    plataforma = models.CharField(max_length=50)  # "facebook", "instagram"
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Link Social"
        verbose_name_plural = "Links Sociais"

    def __str__(self):
        return self.plataforma


class LinkRapido(models.Model):
    secao_rodape = models.ForeignKey(SecaoRodape, on_delete=models.CASCADE, related_name='links_rapidos')
    rotulo = models.CharField(max_length=50)
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Link Rápido"
        verbose_name_plural = "Links Rápidos"

    def __str__(self):
        return self.rotulo


class LinkSuporte(models.Model):
    secao_rodape = models.ForeignKey(SecaoRodape, on_delete=models.CASCADE, related_name='links_suporte')
    rotulo = models.CharField(max_length=50)
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Link de Suporte"
        verbose_name_plural = "Links de Suporte"

    def __str__(self):
        return self.rotulo