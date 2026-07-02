#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegistryTemplate {
pub name: &'static str,
pub description: &'static str,
}

pub fn built_in_templates() -> Vec<RegistryTemplate> {
vec![
RegistryTemplate {
name: "app-tanstack-start-typescript",
description: "TanStack Start TypeScript app stub",
},
RegistryTemplate {
name: "service-rust-axum",
description: "Rust Axum service stub",
},
RegistryTemplate {
name: "service-go-chi",
description: "Go Chi service stub",
},
RegistryTemplate {
name: "service-python-fastapi",
description: "Python FastAPI service stub",
},
RegistryTemplate {
name: "package-typescript",
description: "TypeScript shared package stub",
},
]
}
