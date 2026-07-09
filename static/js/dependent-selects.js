(function () {
  const form = document.querySelector('[data-dependent-selects]');

  if (!form) {
    return;
  }

  const typeSelect = form.querySelector('#id_type');
  const categorySelect = form.querySelector('#id_category');
  const subcategorySelect = form.querySelector('#id_subcategory');

  const replaceOptions = (select, items, placeholder) => {
    select.innerHTML = '';
    select.append(new Option(placeholder, ''));
    items.forEach((item) => {
      select.append(new Option(item.name, item.id));
    });
  };

  const fetchOptions = async (url) => {
    const response = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!response.ok) {
      return [];
    }
    const payload = await response.json();
    return payload.results;
  };

  typeSelect.addEventListener('change', async () => {
    replaceOptions(categorySelect, [], '---------');
    replaceOptions(subcategorySelect, [], '---------');

    if (!typeSelect.value) {
      return;
    }

    const categories = await fetchOptions(`/api/categories/?type=${typeSelect.value}`);
    replaceOptions(categorySelect, categories, '---------');
  });

  categorySelect.addEventListener('change', async () => {
    replaceOptions(subcategorySelect, [], '---------');

    if (!categorySelect.value) {
      return;
    }

    const subcategories = await fetchOptions(`/api/subcategories/?category=${categorySelect.value}`);
    replaceOptions(subcategorySelect, subcategories, '---------');
  });
})();
