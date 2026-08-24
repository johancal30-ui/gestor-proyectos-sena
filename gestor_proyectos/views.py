from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Proyecto, Tarea

def home(request):
    return render(request, 'home.html')

def mostrar_proyectos(request):
    proyectos =  Proyecto.objects.all()
    return render(request, 'proyectos.html', {'proyectos': proyectos})

def nuevos_registros(request):
      Proyecto.objects.create(nombre="Aplicacion bancaria", descripcion="Aplicacion para gestionar cuentas bancarias", duracion=6)
      return HttpResponse("Registro guardado.")

def ver_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    return render(request, 'detalle_proyecto.html', {'proyecto': proyecto})

def nuevo_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        duracion = request.POST.get('duracion')

        if nombre and descripcion and duracion:
            proyecto = Proyecto (
                nombre=nombre,
                descripcion=descripcion,
                duracion=int(duracion),
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
        pass

    datos = {
        'proyecto': proyecto,
        'prioridad_choices': Tarea.PRIORIDAD_CHOICES,
        'estado_choices': Tarea.ESTADO_CHOICES,
    }

    return render(request, 'crear_tarea.html', datos)

