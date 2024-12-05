var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var ESMEvent_1;
import { transform } from "sucrase";
import { ModelEvent, server_event } from "@bokehjs/core/bokeh_events";
import { div } from "@bokehjs/core/dom";
import { isArray } from "@bokehjs/core/util/types";
import { serializeEvent } from "./event-to-object";
import { DOMEvent } from "./html";
import { HTMLBox, HTMLBoxView, set_size } from "./layout";
import { convertUndefined, formatError } from "./util";
import error_css from "../styles/models/esm.css";
const MODULE_CACHE = new Map();
export class DataEvent extends ModelEvent {
    data;
    static __name__ = "DataEvent";
    constructor(data) {
        super();
        this.data = data;
    }
    get event_values() {
        return { model: this.origin, data: this.data };
    }
    static {
        this.prototype.event_name = "data_event";
    }
}
let ESMEvent = class ESMEvent extends DataEvent {
    static { ESMEvent_1 = this; }
    static __name__ = "ESMEvent";
    static from_values(values) {
        const { model, data } = values;
        const event = new ESMEvent_1(data);
        event.origin = model;
        return event;
    }
};
ESMEvent = ESMEvent_1 = __decorate([
    server_event("esm_event")
], ESMEvent);
export { ESMEvent };
export function model_getter(target, name) {
    const model = target.model;
    if (name === "get_child") {
        return (child) => {
            if (!target.accessed_children.includes(child)) {
                target.accessed_children.push(child);
            }
            const child_model = model.data[child];
            if (isArray(child_model)) {
                const children = [];
                for (const subchild of child_model) {
                    children.push(target.get_child_view(subchild)?.el);
                }
                return children;
            }
            else if (model != null) {
                return target.get_child_view(child_model)?.el;
            }
            return null;
        };
    }
    else if (name === "send_msg") {
        return (data) => {
            model.trigger_event(new DataEvent(data));
        };
    }
    else if (name === "send_event") {
        return (name, event) => {
            const serialized = convertUndefined(serializeEvent(event));
            model.trigger_event(new DOMEvent(name, serialized));
        };
    }
    else if (name === "off") {
        return (prop, callback) => {
            const props = isArray(prop) ? prop : [prop];
            for (let p of props) {
                if (p.startsWith("change:")) {
                    p = p.slice("change:".length);
                }
                if (p in model.attributes || p in model.data.attributes) {
                    model.unwatch(target, p, callback);
                    continue;
                }
                else if (p === "msg:custom") {
                    target.remove_on_event(callback);
                    continue;
                }
                if (p.startsWith("lifecycle:")) {
                    p = p.slice("lifecycle:".length);
                }
                if (target._lifecycle_handlers.has(p)) {
                    const handlers = target._lifecycle_handlers.get(p);
                    if (handlers && handlers.includes(callback)) {
                        target._lifecycle_handlers.set(p, handlers.filter(v => v !== callback));
                    }
                    continue;
                }
                console.warn(`Could not unregister callback for event type '${p}'`);
            }
        };
    }
    else if (name === "on") {
        return (prop, callback) => {
            const props = isArray(prop) ? prop : [prop];
            for (let p of props) {
                if (p.startsWith("change:")) {
                    p = p.slice("change:".length);
                }
                if (p in model.attributes || p in model.data.attributes) {
                    model.watch(target, p, callback);
                    continue;
                }
                else if (p === "msg:custom") {
                    target.on_event(callback);
                    continue;
                }
                if (p.startsWith("lifecycle:")) {
                    p = p.slice("lifecycle:".length);
                }
                if (target._lifecycle_handlers.has(p)) {
                    (target._lifecycle_handlers.get(p) || []).push(callback);
                    continue;
                }
                console.warn(`Could not register callback for event type '${p}'`);
            }
        };
    }
    else if (Reflect.has(model.data, name)) {
        if (name in model.data.attributes && !target.accessed_properties.includes(name)) {
            target.accessed_properties.push(name);
        }
        return Reflect.get(model.data, name);
    }
    else if (Reflect.has(model, name)) {
        return Reflect.get(model, name);
    }
    return undefined;
}
export function model_setter(target, name, value) {
    const model = target.model;
    if (Reflect.has(model.data, name)) {
        return Reflect.set(model.data, name, value);
    }
    else if (Reflect.has(model, name)) {
        return Reflect.set(model, name, value);
    }
    return false;
}
function init_model_getter(target, name) {
    if (Reflect.has(target.data, name)) {
        return Reflect.get(target.data, name);
    }
    else if (Reflect.has(target, name)) {
        return Reflect.get(target, name);
    }
}
function init_model_setter(target, name, value) {
    if (Reflect.has(target.data, name)) {
        return Reflect.set(target.data, name, value);
    }
    else if (Reflect.has(target, name)) {
        return Reflect.set(target, name, value);
    }
    return false;
}
export class ReactiveESMView extends HTMLBoxView {
    static __name__ = "ReactiveESMView";
    container;
    accessed_properties = [];
    accessed_children = [];
    compiled_module = null;
    model_proxy;
    render_module = null;
    _changing = false;
    _child_callbacks;
    _child_rendered = new Map();
    _event_handlers = [];
    _lifecycle_handlers = new Map([
        ["after_layout", []],
        ["after_render", []],
        ["resize", []],
        ["remove", []],
    ]);
    _module_cache = MODULE_CACHE;
    _rendered = false;
    _stale_children = false;
    initialize() {
        super.initialize();
        this.model_proxy = new Proxy(this, {
            get: model_getter,
            set: model_setter,
        });
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        this.compiled_module = await this.model.compiled_module;
    }
    stylesheets() {
        const stylesheets = super.stylesheets();
        if (this.model.dev) {
            stylesheets.push(error_css);
        }
        return stylesheets;
    }
    connect_signals() {
        super.connect_signals();
        const { esm, importmap, class_name } = this.model.properties;
        this.on_change([esm, importmap], async () => {
            this.compiled_module = await this.model.compiled_module;
            this.invalidate_render();
        });
        this.on_change(class_name, () => {
            this.container.className = this.model.class_name;
        });
        const child_props = this.model.children.map((child) => this.model.data.properties[child]);
        this.on_change(child_props, () => {
            this.update_children();
        });
        this.model.on_event(ESMEvent, (event) => {
            for (const cb of this._event_handlers) {
                cb(event.data);
            }
        });
    }
    disconnect_signals() {
        super.disconnect_signals();
        this._child_callbacks = new Map();
        this.model.disconnect_watchers(this);
    }
    on_event(callback) {
        this._event_handlers.push(callback);
    }
    remove_on_event(callback) {
        if (this._event_handlers.includes(callback)) {
            this._event_handlers = this._event_handlers.filter((item) => item !== callback);
            return true;
        }
        return false;
    }
    get_child_view(model) {
        return this._child_views.get(model);
    }
    get render_fn() {
        if (this.compiled_module === null) {
            return null;
        }
        else if (this.compiled_module.default) {
            return this.compiled_module.default.render;
        }
        else {
            return this.compiled_module.render;
        }
    }
    get child_models() {
        const children = [];
        for (const child of this.model.children) {
            const model = this.model.data[child];
            if (isArray(model)) {
                for (const subchild of model) {
                    children.push(subchild);
                }
            }
            else if (model != null) {
                children.push(model);
            }
        }
        return children;
    }
    render_error(error) {
        const error_div = div({ class: "error" });
        error_div.innerHTML = formatError(error, this.model.esm);
        this.container.appendChild(error_div);
    }
    render() {
        this.empty();
        this._update_stylesheets();
        this._update_css_classes();
        this._apply_styles();
        this._apply_visible();
        this._child_callbacks = new Map();
        this._child_rendered.clear();
        this._rendered = false;
        set_size(this.el, this.model);
        this.container = div();
        this.container.className = this.model.class_name;
        set_size(this.container, this.model, false);
        this.shadow_el.append(this.container);
        if (this.model.compile_error) {
            this.render_error(this.model.compile_error);
        }
        else {
            const code = this._render_code();
            const render_url = URL.createObjectURL(new Blob([code], { type: "text/javascript" }));
            // @ts-ignore
            this.render_module = importShim(render_url);
            this.render_esm();
        }
    }
    _render_code() {
        return `
const view = Bokeh.index.find_one_by_id('${this.model.id}')

function render() {
  const output = view.render_fn({
    view: view, model: view.model_proxy, data: view.model.data, el: view.container
  })

  Promise.resolve(output).then((out) => {
    if (out instanceof Element) {
      view.container.replaceChildren(out)
    }
    view.after_rendered()
  })
}

export default {render}`;
    }
    after_rendered() {
        const handlers = (this._lifecycle_handlers.get("after_render") || []);
        for (const cb of handlers) {
            cb();
        }
        this.render_children();
        this.model_proxy.on(this.accessed_children, () => { this._stale_children = true; });
        if (!this._rendered) {
            for (const cb of (this._lifecycle_handlers.get("after_layout") || [])) {
                cb();
            }
        }
        this._rendered = true;
    }
    render_esm() {
        if (this.model.compiled === null || this.render_module === null) {
            return;
        }
        this.accessed_properties = [];
        for (const lf of this._lifecycle_handlers.keys()) {
            (this._lifecycle_handlers.get(lf) || []).splice(0);
        }
        this.model.disconnect_watchers(this);
        this.render_module.then((mod) => mod.default.render());
    }
    render_children() {
        for (const child of this.model.children) {
            const child_model = this.model.data[child];
            const children = isArray(child_model) ? child_model : [child_model];
            for (const subchild of children) {
                const view = this._child_views.get(subchild);
                if (!view) {
                    continue;
                }
                const parent = view.el.parentNode;
                if (parent && !this._child_rendered.has(view)) {
                    view.render();
                    this._child_rendered.set(view, true);
                }
            }
        }
        this.r_after_render();
    }
    remove() {
        super.remove();
        for (const cb of (this._lifecycle_handlers.get("remove") || [])) {
            cb();
        }
        this._child_callbacks.clear();
        this._child_rendered.clear();
    }
    after_resize() {
        super.after_resize();
        if (this._rendered && !this._changing) {
            for (const cb of (this._lifecycle_handlers.get("resize") || [])) {
                cb();
            }
        }
    }
    after_layout() {
        super.after_layout();
        if (this._rendered && !this._changing) {
            for (const cb of (this._lifecycle_handlers.get("after_layout") || [])) {
                cb();
            }
        }
    }
    _lookup_child(child_view) {
        for (const child of this.model.children) {
            let models = this.model.data[child];
            models = isArray(models) ? models : [models];
            for (const model of models) {
                if (model === child_view.model) {
                    return child;
                }
            }
        }
        return null;
    }
    async update_children() {
        const created_children = new Set(await this.build_child_views());
        const all_views = this.child_views;
        for (const child_view of all_views) {
            child_view.el.remove();
        }
        const new_views = new Map();
        for (const child_view of this.child_views) {
            if (!created_children.has(child_view)) {
                continue;
            }
            const child = this._lookup_child(child_view);
            if (!child) {
                continue;
            }
            if (new_views.has(child)) {
                new_views.get(child).push(child_view);
            }
            else {
                new_views.set(child, [child_view]);
            }
        }
        for (const view of this._child_rendered.keys()) {
            if (!all_views.includes(view)) {
                this._child_rendered.delete(view);
            }
        }
        for (const child of this.model.children) {
            const callbacks = this._child_callbacks.get(child) || [];
            const new_children = new_views.get(child) || [];
            for (const callback of callbacks) {
                callback(new_children);
            }
        }
        if (this._stale_children) {
            this.render_esm();
            this._stale_children = false;
        }
        this._update_children();
        this.invalidate_layout();
    }
    on_child_render(child, callback) {
        if (!this._child_callbacks.has(child)) {
            this._child_callbacks.set(child, []);
        }
        const callbacks = this._child_callbacks.get(child) || [];
        callbacks.push(callback);
    }
    remove_on_child_render(child) {
        this._child_callbacks.delete(child);
    }
}
export class ReactiveESM extends HTMLBox {
    static __name__ = "ReactiveESM";
    compiled = null;
    compiled_module = null;
    compile_error = null;
    model_proxy;
    sucrase_transforms = ["typescript"];
    _destroyer = null;
    _esm_watchers = {};
    constructor(attrs) {
        super(attrs);
    }
    initialize() {
        super.initialize();
        this.model_proxy = new Proxy(this, {
            get: init_model_getter,
            set: init_model_setter,
        });
        this.recompile();
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.properties.esm.change, () => this.recompile());
        this.connect(this.properties.importmap.change, () => this.recompile());
    }
    watch(view, prop, cb) {
        if (prop in this._esm_watchers) {
            this._esm_watchers[prop].push([view, cb]);
        }
        else {
            this._esm_watchers[prop] = [[view, cb]];
        }
        if (prop in this.data.properties) {
            this.data.property(prop).change.connect(cb);
        }
        else if (prop in this.properties) {
            this.property(prop).change.connect(cb);
        }
    }
    unwatch(view, prop, cb) {
        if (!(prop in this._esm_watchers)) {
            return false;
        }
        const remaining = [];
        for (const [wview, wcb] of this._esm_watchers[prop]) {
            if (wview !== view || wcb !== cb) {
                remaining.push([wview, cb]);
            }
        }
        if (remaining.length > 0) {
            this._esm_watchers[prop] = remaining;
        }
        else {
            delete this._esm_watchers[prop];
        }
        if (prop in this.data.properties) {
            return this.data.property(prop).change.disconnect(cb);
        }
        else if (prop in this.properties) {
            return this.property(prop).change.disconnect(cb);
        }
        return false;
    }
    disconnect_watchers(view) {
        for (const p in this._esm_watchers) {
            const prop = this.data.properties[p];
            const remaining = [];
            for (const [wview, cb] of this._esm_watchers[p]) {
                if (wview === view) {
                    prop.change.disconnect(cb);
                }
                else {
                    remaining.push([wview, cb]);
                }
            }
            if (remaining.length > 0) {
                this._esm_watchers[p] = remaining;
            }
            else {
                delete this._esm_watchers[p];
            }
        }
    }
    _declare_importmap() {
        if (this.importmap) {
            const importMap = { ...this.importmap };
            try {
                // @ts-ignore
                importShim.addImportMap(importMap);
            }
            catch (e) {
                console.warn(`Failed to add import map: ${e}`);
            }
        }
    }
    _run_initializer(initialize) {
        const props = { model: this.model_proxy };
        this._destroyer = initialize(props);
    }
    destroy() {
        super.destroy();
        if (this._destroyer) {
            this._destroyer(this.model_proxy);
        }
    }
    compile() {
        if (this.bundle != null) {
            return this.esm;
        }
        let compiled;
        try {
            compiled = transform(this.esm, {
                transforms: this.sucrase_transforms,
                filePath: "render.tsx",
            }).code;
        }
        catch (e) {
            if (e instanceof SyntaxError && this.dev) {
                this.compile_error = e;
                return null;
            }
            else {
                throw e;
            }
        }
        return compiled;
    }
    async recompile() {
        this.compile_error = null;
        const compiled = this.compile();
        if (compiled === null) {
            this.compiled_module = Promise.resolve(null);
            return;
        }
        this.compiled = compiled;
        this._declare_importmap();
        let esm_module;
        const use_cache = (!this.dev || this.bundle);
        const cache_key = (this.bundle === "url") ? this.esm : (this.bundle || `${this.class_name}-${this.esm.length}`);
        let resolve;
        if (use_cache && MODULE_CACHE.has(cache_key)) {
            esm_module = Promise.resolve(MODULE_CACHE.get(cache_key));
        }
        else {
            if (use_cache) {
                MODULE_CACHE.set(cache_key, new Promise((res) => { resolve = res; }));
            }
            let url;
            if (this.bundle === "url") {
                const parts = location.pathname.split("/");
                let path = parts.slice(0, parts.length - 1).join("/");
                if (path.length) {
                    path += "/";
                }
                url = `${location.origin}/${path}${this.esm}`;
            }
            else {
                url = URL.createObjectURL(new Blob([this.compiled], { type: "text/javascript" }));
            }
            esm_module = window.importShim(url);
        }
        this.compiled_module = esm_module.then((mod) => {
            if (resolve) {
                resolve(mod);
            }
            try {
                let initialize;
                if (this.bundle != null && (mod.default || {}).hasOwnProperty(this.name)) {
                    mod = mod.default[this.name];
                }
                if (mod.initialize) {
                    initialize = mod.initialize;
                }
                else if (mod.default && mod.default.initialize) {
                    initialize = mod.default.initialize;
                }
                else if (typeof mod.default === "function") {
                    const initialized = mod.default();
                    mod = { default: initialized };
                    initialize = initialized.initialize;
                }
                if (initialize) {
                    this._run_initializer(initialize);
                }
                return mod;
            }
            catch (e) {
                if (this.dev) {
                    this.compile_error = e;
                }
                console.error(`Could not initialize module due to error: ${e}`);
                return null;
            }
        });
    }
    static __module__ = "panel.models.esm";
    static {
        this.prototype.default_view = ReactiveESMView;
        this.define(({ Any, Array, Bool, Nullable, Str }) => ({
            bundle: [Nullable(Str), null],
            children: [Array(Str), []],
            class_name: [Str, ""],
            data: [Any],
            dev: [Bool, false],
            esm: [Str, ""],
            importmap: [Any, {}],
        }));
    }
}
//# sourceMappingURL=reactive_esm.js.map