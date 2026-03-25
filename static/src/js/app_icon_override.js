/** @odoo-module **/

const iconMap = {
    sale_management: "sales",
    crm: "crm",
    stock: "inventory",
    account: "accounting",
    purchase: "purchase",
    point_of_sale: "point_of_sale",
    pos_restaurant: "kitchen_display",
    project: "projects",
    mrp: "manufacturing",
    hr: "employee",
    hr_expense: "expenses",
    website: "website",
    documents: "documents",
    web_studio: "apps",
    mass_mailing: "email_marketing",
    equity: "accounting",
    timesheet_grid: "timesheets",
    appointment: "appointment",
    recruitment: "recruitment",
    maintenance: "maintenance",
    field_service: "field_service",
};

function getReplacementIcon(moduleName) {
    const fileBase = iconMap[moduleName];
    if (!fileBase) {
        return null;
    }
    return `/icon_rebrand/static/icons/${fileBase}.png`;
}

function patchAppIcons(root = document) {
    const appNodes = root.querySelectorAll("[data-menu-xmlid], [data-module], .o_app, .o_app_info");
    for (const node of appNodes) {
        const moduleName = node.dataset.module || node.dataset.menuXmlid?.split(".")[0];
        const iconUrl = moduleName ? getReplacementIcon(moduleName) : null;
        if (!iconUrl) {
            continue;
        }

        const image = node.querySelector("img");
        if (image) {
            image.src = iconUrl;
            image.srcset = iconUrl;
        }

        node.style.setProperty("--app-icon", `url(${iconUrl})`);
    }
}

const observer = new MutationObserver(() => patchAppIcons());

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        patchAppIcons();
        observer.observe(document.body, { childList: true, subtree: true });
    });
} else {
    patchAppIcons();
    observer.observe(document.body, { childList: true, subtree: true });
}
