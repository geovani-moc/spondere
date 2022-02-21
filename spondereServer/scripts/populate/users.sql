insert  into users 
    (username, "password", email, fullname, disabled, professor, student, administrator) 
values 
    --administradores
    ('julia', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'julia@facu.gov.br', 'julia pimenta', false, false, false, true),
    --professores
    ('geo', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'geo@facu.gov.br', 'Geovani Pereira', false, true, false, false),
    ('marcos', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'marcos@facu.gov.br', 'Marcos Silva', false, true, false, false),
    ('joao', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'joao@facu.gov.br', 'joao alves', false, true, false, false),
    ('carla', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'carla@facu.gov.br', 'Carla kalorine', false, true, false, false),
    ('carrol', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'CarrolRaymond@facu.gov.br', 'Carrol Raymond', false, true, false, false),
    --alunos
    ('silvio', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'silvio@facu.gov.br', 'Silvio Alencar', false, false, true, false),
    ('wander', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'wander@facu.gov.br', 'Wander antonio', false, false, true, false),
    ('james', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'james@facu.gov.br', 'James Warman', false, false, true, false),
    ('antonio', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'antonio@facu.gov.br', 'Antonio Melo', false, false, true, false),
    ('jessica', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'jessica@facu.gov.br', 'Jessica Pereira', false, false, true, false),
    ('tyrrell', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'TyrrellKitchens@facu.gov.br', 'Tyrrell Kitchens', false, false, true, false),
    ('ruth', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'RuthFrancesco @facu.gov.br', 'Ruth Francesco', false, false, true, false),
    ('orlando', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'OrlandoQuesada@facu.gov.br', 'Orlando Quesada', false, false, true, false),
    ('Amirani', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'AmiraniCamden @facu.gov.br', 'Amirani Camden ', false, false, true, false),   
    ('maria', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'MariaKelsey@facu.gov.br', 'Maria Kelsey', false, false, true, false),   
    ('tristram', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'TristramToninho@facu.gov.br', 'Tristram Toninho', false, false, true, false),
    ('almir', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'AlmirSgro@facu.gov.br', 'Almir Sgro', false, false, true, false),   
    ('kelleigh', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'KelleighCornelio@facu.gov.br', 'Kelleigh Cornelio', false, false, true, false),   
    ('flavia', '$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42', 'FlaviaMiles@facu.gov.br', 'Flavia Miles', false, false, true, false);