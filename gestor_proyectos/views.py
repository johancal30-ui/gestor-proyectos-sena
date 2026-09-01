from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Proyecto, Tarea

@login_required
def home(request):
    return render(request, 'home.html')

def acerca_de(request):
    return render(request, 'acerca-de.html')

def mostrar_proyectos(request):
    proyectos =  Proyecto.objects.all()
    return render(request, 'proyectos.html', {'proyectos': proyectos})

def nuevos_registros(request):
      Proyecto.objects.create(nombre="Aplicacion bancaria", descripcion="Aplicacion para gestionar cuentas bancarias", duracion=6)
      return HttpResponse("Registro guardado.")

def ver_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    print(proyecto.tareas.all)
    return render(request, 'detalle_proyecto.html', {'proyecto': proyecto})

def nuevo_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        duracion = request.POST.get('duracion')
        imagen = request.FILES.get('imagen')

        if nombre and descripcion and duracion:
            proyecto = Proyecto (
                nombre=nombre,
                descripcion=descripcion,
                duracion=int(duracion),
                imagen = imagen
                )
            proyecto.save()

            return redirect('proyectos')

    return render(request, 'nuevo_proyecto.html')

def eliminar_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    proyecto.delete()
    return redirect('proyectos')

def editar_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        duracion = request.POST.get('duracion')

        if nombre and descripcion and duracion:
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.duracion = int(duracion)
            proyecto.save()
            return redirect('ver_proyecto', id=proyecto.id)

    return render(request, 'editar_proyecto.html', {'proyecto': proyecto})

def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)


    if request.method == "POST":
        titulo = request.POST.get('titulo').strip()
        prioridad = request.POST.get('prioridad')
        estado = request.POST.get('estado')

        if titulo: 
            tarea = Tarea(titulo= titulo, 
                          prioridad=prioridad, 
                          estado=estado, 
                          proyecto=proyecto)
            tarea.save()

            return redirect('ver_proyecto', id=proyecto_id)
        

    datos = {
        'proyecto': proyecto,
        'prioridad_choices': Tarea.PRIORIDAD_CHOICES,
        'estado_choices': Tarea.ESTADO_CHOICES,
    }

    return render(request, 'crear_tarea.html', datos)

def avanzar_estado_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)

    if tarea.estado == "PENDIENTE":
        tarea.estado = "EN_PROGRESO"
        tarea.save()

    elif tarea.estado == "EN_PROGRESO":
        tarea.estado = "COMPLETADA"
        tarea.save()

    return redirect('ver_proyecto', id=tarea.proyecto.id)

@require_POST
def completar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)

    if tarea.estado != "COMPLETADA":
        tarea.estado = "COMPLETADA"
        tarea.save()

    return redirect("ver_proyecto", id= tarea.proyecto.id)

def eliminar_tarea(request, id):
    tarea= get_object_or_404(Tarea, id=id)

    id_proyecto = tarea.proyecto.id
    tarea.delete()
    return redirect ('ver_proyecto', id=id_proyecto)