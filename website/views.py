from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import MatriculaForm
from .models import Matricula, Curso
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

def home(request):
    """
    View principal que carrega todas as seções da página inicial.
    """
    # Hero (singleton)
    hero = SecaoHero.objects.first()
    imagens_carrossel = ImagemCarrossel.objects.filter(secao_hero=hero).order_by('-ativo', 'id') if hero else []

    # Estatísticas
    estatisticas = SecaoEstatisticas.objects.first()
    itens_estatistica = ItemEstatistica.objects.filter(secao_estatisticas=estatisticas) if estatisticas else []

    # Cursos
    secao_cursos = SecaoCursos.objects.first()
    cursos = Curso.objects.filter(secao_cursos=secao_cursos) if secao_cursos else []

    # Sobre
    sobre = SecaoSobre.objects.first()

    # Infraestrutura
    secao_infra = SecaoInfraestrutura.objects.first()
    itens_infra = ItemInfraestrutura.objects.filter(secao_infraestrutura=secao_infra) if secao_infra else []

    # Depoimentos
    secao_depoimentos = SecaoDepoimentos.objects.first()
    depoimentos = Depoimento.objects.filter(secao_depoimentos=secao_depoimentos) if secao_depoimentos else []

    # Matrículas
    matriculas = SecaoMatriculas.objects.first()

    # Contacto
    contacto = InformacaoContacto.objects.first()

    # Rodapé
    rodape = SecaoRodape.objects.first()
    links_sociais = LinkSocial.objects.filter(secao_rodape=rodape) if rodape else []
    links_rapidos = LinkRapido.objects.filter(secao_rodape=rodape) if rodape else []
    links_suporte = LinkSuporte.objects.filter(secao_rodape=rodape) if rodape else []

    context = {
        'hero': hero,
        'imagens_carrossel': imagens_carrossel,
        'itens_estatistica': itens_estatistica,
        'secao_cursos': secao_cursos,
        'cursos': cursos,
        'sobre': sobre,
        'itens_infra': itens_infra,
        'secao_infra': secao_infra,
        'depoimentos': depoimentos,
        'secao_depoimentos': secao_depoimentos,
        'matriculas': matriculas,
        'contacto': contacto,
        'rodape': rodape,
        'links_sociais': links_sociais,
        'links_rapidos': links_rapidos,
        'links_suporte': links_suporte,
    }
    return render(request, 'web/index.html', context)


def curso_detalhe(request, curso_id):
    """
    View para exibir os detalhes de um curso específico.
    """
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'web/curso_detalhe.html', {'curso': curso})


def matricula_create(request):
    """
    View para exibir formulário de matrícula e processar a inscrição.
    """
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save()
            messages.success(
                request,
                f'Matrícula realizada com sucesso! {matricula.nome_completo}, '
                f'você está pré-inscrito no curso {matricula.curso.nome}. '
                'Aguarde nosso contato para confirmação.'
            )
            return redirect('matricula_sucesso', matricula_id=matricula.id)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Se houver um curso_id na URL, pré-seleciona o curso
        curso_id = request.GET.get('curso')
        initial = {}
        if curso_id:
            try:
                curso = Curso.objects.get(id=curso_id)
                initial['curso'] = curso
            except Curso.DoesNotExist:
                pass
        form = MatriculaForm(initial=initial)

    # Buscar a lista de cursos para exibir no template (se necessário)
    cursos = Curso.objects.all().order_by('nome')

    context = {
        'form': form,
        'cursos': cursos,
        'titulo': 'Matrícula - Instituto Educativo',
    }
    return render(request, 'web/matricula_form.html', context)


def matricula_sucesso(request, matricula_id):
    """
    Página de confirmação após a matrícula.
    """
    matricula = get_object_or_404(Matricula, id=matricula_id)
    return render(request, 'web/matricula_sucesso.html', {'matricula': matricula})