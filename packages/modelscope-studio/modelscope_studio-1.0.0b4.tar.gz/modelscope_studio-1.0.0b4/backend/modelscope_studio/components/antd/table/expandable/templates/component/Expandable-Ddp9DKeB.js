import { g as X, b as Y } from "./Index-Cd2jgCTM.js";
function Z(e) {
  return e === void 0;
}
function k() {
}
function v(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function V(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function y(e) {
  let t;
  return V(e, (r) => t = r)(), t;
}
const P = [];
function b(e, t = k) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (v(e, c) && (e = c, r)) {
      const f = !P.length;
      for (const a of n)
        a[1](), P.push(a, e);
      if (f) {
        for (let a = 0; a < P.length; a += 2)
          P[a][0](P[a + 1]);
        P.length = 0;
      }
    }
  }
  function s(c) {
    i(c(e));
  }
  function o(c, f = k) {
    const a = [c, f];
    return n.add(a), n.size === 1 && (r = t(i, s) || k), c(e), () => {
      n.delete(a), n.size === 0 && r && (r(), r = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: o
  };
}
const {
  getContext: N,
  setContext: h
} = window.__gradio__svelte__internal, $ = "$$ms-gr-slots-key";
function ee() {
  const e = b({});
  return h($, e);
}
const te = "$$ms-gr-render-slot-context-key";
function ne() {
  const e = h(te, b({}));
  return (t, r) => {
    e.update((n) => typeof r == "function" ? {
      ...n,
      [t]: r(n[t])
    } : {
      ...n,
      [t]: r
    });
  };
}
const se = "$$ms-gr-context-key";
function j(e) {
  return Z(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const G = "$$ms-gr-sub-index-context-key";
function re() {
  return N(G) || null;
}
function T(e) {
  return h(G, e);
}
function oe(e, t, r) {
  var g, x;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = J(), i = ue({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = re();
  typeof s == "number" && T(void 0), typeof e._internal.subIndex == "number" && T(e._internal.subIndex), n && n.subscribe((l) => {
    i.slotKey.set(l);
  }), ie();
  const o = N(se), c = ((g = y(o)) == null ? void 0 : g.as_item) || e.as_item, f = j(o ? c ? ((x = y(o)) == null ? void 0 : x[c]) || {} : y(o) || {} : {}), a = (l, m) => l ? X({
    ...l,
    ...m || {}
  }, t) : void 0, d = b({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    ...f,
    restProps: a(e.restProps, f),
    originalRestProps: e.restProps
  });
  return o ? (o.subscribe((l) => {
    const {
      as_item: m
    } = y(d);
    m && (l = l == null ? void 0 : l[m]), l = j(l), d.update((_) => ({
      ..._,
      ...l || {},
      restProps: a(_.restProps, l)
    }));
  }), [d, (l) => {
    var _;
    const m = j(l.as_item ? ((_ = y(o)) == null ? void 0 : _[l.as_item]) || {} : y(o) || {});
    return d.set({
      ...l,
      _internal: {
        ...l._internal,
        index: s ?? l._internal.index
      },
      ...m,
      restProps: a(l.restProps, m),
      originalRestProps: l.restProps
    });
  }]) : [d, (l) => {
    d.set({
      ...l,
      _internal: {
        ...l._internal,
        index: s ?? l._internal.index
      },
      restProps: a(l.restProps),
      originalRestProps: l.restProps
    });
  }];
}
const H = "$$ms-gr-slot-key";
function ie() {
  h(H, b(void 0));
}
function J() {
  return N(H);
}
const le = "$$ms-gr-component-slot-context-key";
function ue({
  slot: e,
  index: t,
  subIndex: r
}) {
  return h(le, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(r)
  });
}
function K(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ce(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var L = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function r() {
      for (var s = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (s = i(s, n(c)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return r.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var o = "";
      for (var c in s)
        t.call(s, c) && s[c] && (o = i(o, c));
      return o;
    }
    function i(s, o) {
      return o ? s ? s + " " + o : s + o : s;
    }
    e.exports ? (r.default = r, e.exports = r) : window.classNames = r;
  })();
})(L);
var ae = L.exports;
const de = /* @__PURE__ */ ce(ae), {
  getContext: fe,
  setContext: me
} = window.__gradio__svelte__internal;
function _e(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function r(i = ["default"]) {
    const s = i.reduce((o, c) => (o[c] = b([]), o), {});
    return me(t, {
      itemsMap: s,
      allowedSlots: i
    }), s;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: s
    } = fe(t);
    return function(o, c, f) {
      i && (o ? i[o].update((a) => {
        const d = [...a];
        return s.includes(o) ? d[c] = f : d[c] = void 0, d;
      }) : s.includes("default") && i.default.update((a) => {
        const d = [...a];
        return d[c] = f, d;
      }));
    };
  }
  return {
    getItems: r,
    getSetItemFn: n
  };
}
const {
  getItems: Fe,
  getSetItemFn: be
} = _e("table-expandable"), {
  SvelteComponent: pe,
  assign: z,
  check_outros: ge,
  component_subscribe: E,
  compute_rest_props: D,
  create_slot: xe,
  detach: ye,
  empty: U,
  exclude_internal_props: Pe,
  flush: p,
  get_all_dirty_from_scope: he,
  get_slot_changes: Ie,
  group_outros: Se,
  init: Ce,
  insert_hydration: Re,
  safe_not_equal: Ke,
  transition_in: w,
  transition_out: F,
  update_slot_base: Ee
} = window.__gradio__svelte__internal;
function B(e) {
  let t;
  const r = (
    /*#slots*/
    e[17].default
  ), n = xe(
    r,
    e,
    /*$$scope*/
    e[16],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(i) {
      n && n.l(i);
    },
    m(i, s) {
      n && n.m(i, s), t = !0;
    },
    p(i, s) {
      n && n.p && (!t || s & /*$$scope*/
      65536) && Ee(
        n,
        r,
        i,
        /*$$scope*/
        i[16],
        t ? Ie(
          r,
          /*$$scope*/
          i[16],
          s,
          null
        ) : he(
          /*$$scope*/
          i[16]
        ),
        null
      );
    },
    i(i) {
      t || (w(n, i), t = !0);
    },
    o(i) {
      F(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function ke(e) {
  let t, r, n = (
    /*$mergedProps*/
    e[0].visible && B(e)
  );
  return {
    c() {
      n && n.c(), t = U();
    },
    l(i) {
      n && n.l(i), t = U();
    },
    m(i, s) {
      n && n.m(i, s), Re(i, t, s), r = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && w(n, 1)) : (n = B(i), n.c(), w(n, 1), n.m(t.parentNode, t)) : n && (Se(), F(n, 1, 1, () => {
        n = null;
      }), ge());
    },
    i(i) {
      r || (w(n), r = !0);
    },
    o(i) {
      F(n), r = !1;
    },
    d(i) {
      i && ye(t), n && n.d(i);
    }
  };
}
function we(e, t, r) {
  const n = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = D(t, n), s, o, c, f, {
    $$slots: a = {},
    $$scope: d
  } = t, {
    gradio: g
  } = t, {
    props: x = {}
  } = t;
  const l = b(x);
  E(e, l, (u) => r(15, f = u));
  let {
    _internal: m = {}
  } = t, {
    as_item: _
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: C = []
  } = t, {
    elem_style: R = {}
  } = t;
  const O = J();
  E(e, O, (u) => r(14, c = u));
  const [q, Q] = oe({
    gradio: g,
    props: f,
    _internal: m,
    visible: I,
    elem_id: S,
    elem_classes: C,
    elem_style: R,
    as_item: _,
    restProps: i
  });
  E(e, q, (u) => r(0, o = u));
  const A = ee();
  E(e, A, (u) => r(13, s = u));
  const M = ne(), W = be();
  return e.$$set = (u) => {
    t = z(z({}, t), Pe(u)), r(21, i = D(t, n)), "gradio" in u && r(5, g = u.gradio), "props" in u && r(6, x = u.props), "_internal" in u && r(7, m = u._internal), "as_item" in u && r(8, _ = u.as_item), "visible" in u && r(9, I = u.visible), "elem_id" in u && r(10, S = u.elem_id), "elem_classes" in u && r(11, C = u.elem_classes), "elem_style" in u && r(12, R = u.elem_style), "$$scope" in u && r(16, d = u.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    64 && l.update((u) => ({
      ...u,
      ...x
    })), Q({
      gradio: g,
      props: f,
      _internal: m,
      visible: I,
      elem_id: S,
      elem_classes: C,
      elem_style: R,
      as_item: _,
      restProps: i
    }), e.$$.dirty & /*$mergedProps, $slotKey, $slots*/
    24577) {
      const u = Y(o);
      W(c, o._internal.index || 0, {
        props: {
          style: o.elem_style,
          className: de(o.elem_classes, "ms-gr-antd-table-expandable"),
          id: o.elem_id,
          ...o.restProps,
          ...o.props,
          ...u,
          expandedRowClassName: K(o.props.expandedRowClassName || o.restProps.expandedRowClassName),
          expandedRowRender: K(o.props.expandedRowRender || o.restProps.expandedRowRender),
          rowExpandable: K(o.props.rowExpandable || o.restProps.rowExpandable),
          expandIcon: K(o.props.expandIcon || o.restProps.expandIcon),
          columnTitle: o.props.columnTitle || o.restProps.columnTitle
        },
        slots: {
          ...s,
          expandIcon: {
            el: s.expandIcon,
            callback: M,
            clone: !0
          },
          expandedRowRender: {
            el: s.expandedRowRender,
            callback: M,
            clone: !0
          }
        }
      });
    }
  }, [o, l, O, q, A, g, x, m, _, I, S, C, R, s, c, f, d, a];
}
class Ne extends pe {
  constructor(t) {
    super(), Ce(this, t, we, ke, Ke, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      visible: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), p();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), p();
  }
}
export {
  Ne as default
};
