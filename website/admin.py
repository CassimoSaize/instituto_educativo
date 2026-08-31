from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from .models import Matricula


from .models import (
    SecaoHero, ImagemCarrossel,
    SecaoEstatisticas, ItemEstatistica,
    SecaoCursos, Curso,
    SecaoSobre,
    SecaoInfraestrutura, ItemInfraestrutura,
    SecaoDepoimentos, Depoimento,
    SecaoMatriculas,
    InformacaoContacto,
    SecaoRodape, LinkSocial, LinkRapido, LinkSuporte
)


# ---------- INLINES (para editar filhos dentro do pai) ----------
class ImagemCarrosselInline(admin.TabularInline):  # <-- CLASSE INLINE CORRETA
    model = ImagemCarrossel
    extra = 1
    fields = ('imagem', 'alt', 'ativo')
    # Opcional: exibir pré-visualização
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-height: 80px;"/>'
        return "Sem imagem"
    preview.allow_tags = True
    preview.short_description = "Pré-visualização"


class ItemEstatisticaInline(admin.TabularInline):
    model = ItemEstatistica
    extra = 1
    fields = ('numero', 'rotulo', 'descricao')


class CursoInline(admin.TabularInline):
    model = Curso
    extra = 1
    fields = ('nome', 'icone', 'preco', 'duracao', 'imagem')
    ordering = ('nome',)




class ItemInfraestruturaInline(admin.TabularInline):
    model = ItemInfraestrutura
    extra = 1
    fields = ('icone', 'titulo', 'descricao')


class DepoimentoInline(admin.TabularInline):
    model = Depoimento
    extra = 1
    fields = ('autor_nome', 'autor_cargo', 'citacao', 'icone_avatar')


class LinkSocialInline(admin.TabularInline):
    model = LinkSocial
    extra = 1
    fields = ('plataforma', 'url')


class LinkRapidoInline(admin.TabularInline):
    model = LinkRapido
    extra = 1
    fields = ('rotulo', 'url')


class LinkSuporteInline(admin.TabularInline):
    model = LinkSuporte
    extra = 1
    fields = ('rotulo', 'url')


# ---------- ADMIN DAS SEÇÕES SINGLETON (com inlines) ----------
@admin.register(SecaoHero)
class SecaoHeroAdmin(admin.ModelAdmin):
    inlines = [ImagemCarrosselInline]   # <-- USANDO A INLINE, NÃO O MODELADMIN
    fieldsets = (
        ('Conteúdo Principal', {
            'fields': ('titulo', 'subtitulo', 'descricao')
        }),
        ('Preço', {
            'fields': ('preco', 'rotulo_preco', 'info_parcelamento')
        }),
        ('Botões', {
            'fields': (
                'texto_botao_primario', 'link_botao_primario',
                'texto_botao_secundario', 'link_botao_secundario'
            )
        }),
    )
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoEstatisticas)
class SecaoEstatisticasAdmin(admin.ModelAdmin):
    inlines = [ItemEstatisticaInline]
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoCursos)
class SecaoCursosAdmin(admin.ModelAdmin):
    inlines = [CursoInline]
    fieldsets = (
        ('Títulos', {'fields': ('titulo', 'subtitulo')}),
        ('Chamada para Ação', {'fields': ('texto_chamada', 'link_chamada')}),
    )
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoSobre)
class SecaoSobreAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identificação', {'fields': ('texto_distintivo', 'titulo')}),
        ('Conteúdo', {'fields': ('missao', 'visao', 'valores', 'historia')}),
        ('Imagem', {'fields': ('imagem', 'preview_imagem')}),
    )
    readonly_fields = ('preview_imagem',)

    def preview_imagem(self, obj):
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-height: 200px; max-width: 300px;"/>'
        return "Sem imagem"
    preview_imagem.allow_tags = True
    preview_imagem.short_description = "Pré-visualização"

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoInfraestrutura)
class SecaoInfraestruturaAdmin(admin.ModelAdmin):
    inlines = [ItemInfraestruturaInline]
    fields = ('titulo', 'subtitulo')
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoDepoimentos)
class SecaoDepoimentosAdmin(admin.ModelAdmin):
    inlines = [DepoimentoInline]
    fields = ('titulo', 'subtitulo')
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoMatriculas)
class SecaoMatriculasAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Título e Subtítulo', {'fields': ('titulo', 'subtitulo')}),
        ('Botão', {'fields': ('texto_botao', 'link_botao')}),
    )
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(InformacaoContacto)
class InformacaoContactoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contactos', {
            'fields': ('telefone', 'whatsapp', 'email', 'endereco')
        }),
        ('Mapa', {
            'fields': ('url_mapa_embed', 'referencia_mapa')
        }),
    )
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SecaoRodape)
class SecaoRodapeAdmin(admin.ModelAdmin):
    inlines = [LinkSocialInline, LinkRapidoInline, LinkSuporteInline]
    fieldsets = (
        ('Identificação', {'fields': ('nome_instituto', 'descricao')}),
        ('Horário e Copyright', {'fields': ('horario_funcionamento', 'texto_copyright')}),
    )
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


# ---------- ADMIN DOS MODELOS FILHOS (listagens separadas) ----------
@admin.register(ImagemCarrossel)
class ImagemCarrosselAdmin(admin.ModelAdmin):
    list_display = ('alt', 'preview_imagem', 'ativo', 'secao_hero')
    list_filter = ('ativo', 'secao_hero')
    search_fields = ('alt',)
    readonly_fields = ('preview_imagem',)

    def preview_imagem(self, obj):
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-height: 100px; max-width: 150px;"/>'
        return "Sem imagem"
    preview_imagem.allow_tags = True
    preview_imagem.short_description = "Pré-visualização"


@admin.register(ItemEstatistica)
class ItemEstatisticaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'rotulo', 'descricao', 'secao_estatisticas')
    search_fields = ('rotulo', 'numero')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao', 'secao_cursos')
    list_filter = ('secao_cursos',)
    search_fields = ('nome', 'descricao')


@admin.register(ItemInfraestrutura)
class ItemInfraestruturaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'icone', 'secao_infraestrutura')
    search_fields = ('titulo', 'descricao')


@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ('autor_nome', 'autor_cargo', 'secao_depoimentos')
    search_fields = ('autor_nome', 'citacao')


@admin.register(LinkSocial)
class LinkSocialAdmin(admin.ModelAdmin):
    list_display = ('plataforma', 'url', 'secao_rodape')
    list_filter = ('plataforma',)


@admin.register(LinkRapido)
class LinkRapidoAdmin(admin.ModelAdmin):
    list_display = ('rotulo', 'url', 'secao_rodape')


@admin.register(LinkSuporte)
class LinkSuporteAdmin(admin.ModelAdmin):
    list_display = ('rotulo', 'url', 'secao_rodape')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'curso',
        'telefone',
        'email',
        'status_colorido',
        'data_criacao',
        'acoes',
    )
    list_filter = ('curso', 'status', 'forma_pagamento', 'data_criacao')
    search_fields = ('nome_completo', 'bilhete_identidade', 'telefone', 'email')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'genero', 'nacionalidade', 'bilhete_identidade')
        }),
        ('Contacto', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Curso e Pagamento', {
            'fields': ('curso', 'forma_pagamento')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirmar_matriculas', 'aprovar_matriculas', 'imprimir_situacao']

    # ---------- STATUS COLORIDO ----------
    def status_colorido(self, obj):
        """Exibe o status com badge colorido."""
        cores = {
            'P': '#f39c12',  # laranja (pendente)
            'C': '#3498db',  # azul (confirmada)
            'A': '#2ecc71',  # verde (aprovada)
            'R': '#e74c3c',  # vermelho (rejeitada)
            'M': '#9b59b6',  # roxo (matriculado)
        }
        cor = cores.get(obj.status, '#95a5a6')  # cinza por padrão
        status_display = dict(Matricula.STATUS_CHOICES).get(obj.status, 'Desconhecido')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">{}</span>',
            cor,
            status_display
        )
    status_colorido.short_description = 'Status'

    # ---------- AÇÕES RÁPIDAS (botões na listagem) ----------
    def acoes(self, obj):
        """Botões rápidos para confirmar, aprovar ou visualizar."""
        if obj.status == 'P':  # Pendente
            return format_html(
                '<a href="{}" class="button" style="background: #3498db; color: white; padding: 2px 10px; border-radius: 4px; text-decoration: none; margin-right: 4px;">Confirmar</a>'
                '<a href="{}" class="button" style="background: #2ecc71; color: white; padding: 2px 10px; border-radius: 4px; text-decoration: none;">Aprovar</a>',
                reverse('admin:confirmar_matricula', args=[obj.id]),
                reverse('admin:aprovar_matricula', args=[obj.id])
            )
        elif obj.status == 'C':  # Confirmada
            return format_html(
                '<a href="{}" class="button" style="background: #2ecc71; color: white; padding: 2px 10px; border-radius: 4px; text-decoration: none;">Aprovar</a>',
                reverse('admin:aprovar_matricula', args=[obj.id])
            )
        return '-'
    acoes.short_description = 'Ações'

    # ---------- AÇÕES EM MASSA ----------
    def confirmar_matriculas(self, request, queryset):
        queryset.update(status='C')
        self.message_user(request, f'{queryset.count()} matrícula(s) confirmada(s).')
    confirmar_matriculas.short_description = 'Confirmar matrículas selecionadas'

    def aprovar_matriculas(self, request, queryset):
        queryset.update(status='A')
        self.message_user(request, f'{queryset.count()} matrícula(s) aprovada(s).')
    aprovar_matriculas.short_description = 'Aprovar matrículas selecionadas'

    # ---------- IMPRIMIR SITUAÇÃO DO ESTUDANTE ----------
    def imprimir_situacao(self, request, queryset):
        """Gera um relatório em HTML (ou PDF) com a situação de cada estudante selecionado."""
        if queryset.count() == 1:
            # Se for apenas um, redireciona para a página de detalhes
            obj = queryset.first()
            return self._render_situacao_individual(obj)
        else:
            # Para múltiplos, gera um relatório consolidado
            return self._render_relatorio_multiplos(queryset)

    def _render_situacao_individual(self, obj):
        """Renderiza uma página HTML com a situação detalhada de um estudante."""
        contexto = {
            'matricula': obj,
            'status_display': obj.get_status_display(),
            'status_cor': self._get_status_cor(obj.status),
        }
        html_content = render_to_string('admin/matricula_situacao.html', contexto)
        return HttpResponse(html_content)

    def _render_relatorio_multiplos(self, queryset):
        """Renderiza uma lista consolidada de todos os selecionados."""
        contexto = {
            'matriculas': queryset,
            'total': queryset.count(),
        }
        html_content = render_to_string('admin/matricula_relatorio.html', contexto)
        return HttpResponse(html_content)

    def _get_status_cor(self, status):
        """Retorna a cor correspondente ao status."""
        cores = {
            'P': '#f39c12',
            'C': '#3498db',
            'A': '#2ecc71',
            'R': '#e74c3c',
            'M': '#9b59b6',
        }
        return cores.get(status, '#95a5a6')

    imprimir_situacao.short_description = 'Imprimir situação do estudante'

    # ---------- URLS PERSONALIZADAS PARA AÇÕES RÁPIDAS ----------
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'confirmar/<int:matricula_id>/',
                self.admin_site.admin_view(self.confirmar_matricula),
                name='confirmar_matricula',
            ),
            path(
                'aprovar/<int:matricula_id>/',
                self.admin_site.admin_view(self.aprovar_matricula),
                name='aprovar_matricula',
            ),
        ]
        return custom_urls + urls

    def confirmar_matricula(self, request, matricula_id):
        """View para confirmar uma única matrícula via URL."""
        obj = get_object_or_404(Matricula, id=matricula_id)
        obj.status = 'C'
        obj.save()
        self.message_user(request, f'Matrícula de {obj.nome_completo} confirmada.')
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def aprovar_matricula(self, request, matricula_id):
        """View para aprovar uma única matrícula via URL."""
        obj = get_object_or_404(Matricula, id=matricula_id)
        obj.status = 'A'
        obj.save()
        self.message_user(request, f'Matrícula de {obj.nome_completo} aprovada.')
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))