/*===== MENU SHOW =====*/ 
const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}
showMenu('nav-toggle','nav-menu')

/*===== REMOVE MENU MOBILE =====*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*===== SCROLL SECTIONS ACTIVE LINK =====*/
const sections = document.querySelectorAll('section[id]')

window.addEventListener('scroll', scrollActive)

function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight
        const sectionTop = current.offsetTop - 50;
        sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active')
        }else{
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active')
        }
    })
}

/*===== SCROLL REVEAL ANIMATION =====*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '80px',
    duration: 2000,
    reset: true
})

/*SCROLL HOME*/
sr.reveal('.home__title', {})
sr.reveal('.home__scroll', {delay: 200})
sr.reveal('.home__img', {origin:'right', delay: 400})

/*SCROLL ABOUT*/
sr.reveal('.about__img', {delay: 500})
sr.reveal('.about__subtitle', {delay: 300})
sr.reveal('.about__profession', {delay: 400})
sr.reveal('.about__text', {delay: 500})
sr.reveal('.about__social-icon', {delay: 600, interval: 200})

/*SCROLL SKILLS*/
sr.reveal('.skills__subtitle', {})
sr.reveal('.skills__name', {distance: '20px', delay: 50, interval: 100})
sr.reveal('.skills__img', {delay: 400})

/*crsf token*/ 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Busca el token CSRF
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*SCROLL PORTFOLIO*/
sr.reveal('.portfolio__img', {interval: 200})

/*SCROLL CONTACT*/
sr.reveal('.contact__subtitle', {})
sr.reveal('.contact__text', {interval: 200})
sr.reveal('.contact__input', {delay: 400})
sr.reveal('.contact__button', {delay: 600})


function getCoordinates() {
    if (navigator.geolocation) {
      posicion=navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
      console.log("posicion con getcooordinates: "+ posicion)
      //para mirar cambios de ubicacion
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  }

  function geoFindMe(tipo) {
    const status = document.querySelector("#status");
    const mapLink = document.querySelector("#map-link");
  
    mapLink.href = "";
    mapLink.textContent = "";
    
  
    function success(position) {
    
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
  
      status.textContent = "";
      mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
      coordenadas=[latitude,longitude];
      console.log(coordenadas)
      link_mapa=mapLink.href
      mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;
      fetch(url)
            .then(response => response.json())
            .then(data => {
                const direccion = data.display_name;
                console.log("Dirección completa:", direccion);

                const datos = {
                    tipo,
                    coordenadas,
                    direccion,
                    link_mapa,
                };

                // Solicitud POST a la vista de Django para guardar la salida
                fetch("/guardar_ficha/", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF
                    },
                    body: JSON.stringify(datos)
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                        console.log('Se ha realizado la solicitud POST correctamente');
                    })
                    .catch(error => {
                        console.error('Error al enviar los datos');
                    });
            })
            .catch(error => {
                console.log("Error al obtener la dirección:", error);
            });

        console.log("El link del mapa es " + mapLink.href);
        const enlaceMapa = document.getElementById("enlace-mapa");
        enlaceMapa.textContent = mapLink.href;
    }

    function error() {
        status.textContent = "Unable to retrieve your location";
    }

    if (!navigator.geolocation) {
        status.textContent = "Geolocation is not supported by your browser";
    } else {
        status.textContent = "Locating…";
        navigator.geolocation.getCurrentPosition(success, error);
    }

    console.log("Fin geol");
}
  
function detectarCambiosUbicacion(){
    changes_loc=navigator.geolocation.watchPosition(success,error,options)
}

/*window.onload = registrosPorUsuario;

document.addEventListener("DOMContentLoaded", function() {
  // Llama a la función registrosPorUsuario una vez que el DOM esté listo
  registrosPorUsuario();
});*/


function registrosPorUsuario(){
  const filas=document.querySelectorAll('tr[data-username]')
  filas.forEach(fila => {
    const nombreUsuario = fila.getAttribute('data-username');
    fila.addEventListener('click', () => {
        const nombreUsuario = fila.getAttribute('data-username');
        const tipoTabla=fila.getAttribute('data-tipo')
        console.log('clic hecho: haciendo el fetch de get datos', nombreUsuario)
        if (tipoTabla==='entrada'){
          window.location.href = `/entradas_nombre_usuario/${nombreUsuario}?tipo=${tipoTabla}`;
        } else if(tipoTabla==='salida'){
          window.location.href=`/salidas_por_usuario/${nombreUsuario}?tipo=${tipoTabla}`;
        }
        fetch(`/registros_por_usuario/?nombre_usuario=${nombreUsuario}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          } // O 'POST' según la configuración de tu servidor
        })
        .then(response => response.json()) // Suponiendo que el servidor responde con JSON
        .then(data => {
            // Manipula los datos para crear una nueva tabla o mostrarlos de alguna manera
            console.log(data);
        })
        .catch(error => {
            console.error('Error al obtener los registros:', error);
        });
    });
});
}
window.addEventListener("DOMContentLoaded", function() {
  // Llama a la función registrosPorUsuario una vez que el DOM esté listo
  registrosPorUsuario();});



