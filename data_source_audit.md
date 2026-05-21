# Data Source Audit

Verified on 2026-05-21 unless noted otherwise.

Statistics Iceland open-data basis: Statistics Iceland states that all published website content may be reused under CC BY 4.0 with attribution, and that all published statistics are accessible through the API without registration.

## Production-ready PX-Web sources

```yaml
id: statice_cpi
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Efnahagur/Efnahagur__visitolur__1_vnv__1_vnv/VIS01002.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Efnahagur/VIS01002.px
table_id: VIS01002
variables:
  time: Month
  value: Index
  base: Base
unit: Indices
frequency: monthly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses CPI and CPI less housing cost, Base 1988.
```

```yaml
id: cb_new_credit
source: Central Bank of Iceland
source_url: https://indicators.cb.is/statistics/monetary-statistics/
download_url: https://sedlabanki.is/library?itemid=b73e42d6-ba32-4eb3-b39e-1c70d2e45aec
table_id: INN_NY_UTLAN
variables:
  time: Month
  sector: sector / counterparty row
  block: total, non-indexed, indexed, foreign-currency, leasing
unit: ISK million
frequency: monthly
license: Free use with source acknowledgement
attribution: "Source: Central Bank of Iceland"
verified_at: 2026-05-21
notes: Official Central Bank library Excel download verified. MVP uses total new credit less prepayments for households and non-financial corporations, transformed to 12-month rolling-sum YoY growth.
```

```yaml
id: statice_gdp_quarterly
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Efnahagur/Efnahagur__thjodhagsreikningar__landsframl__2_landsframleidsla_arsfj/THJ01601.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Efnahagur/THJ01601.px
table_id: THJ01601
variables:
  time: Ársfjórðungur
  value_unit: Mælikvarði
  category: Skipting
unit: Percent
frequency: quarterly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses volume changes for gross domestic product.
```

```yaml
id: statice_unemployment_quarterly
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Samfelag/Samfelag__vinnumarkadur__vinnumarkadsrannsokn__2_arsfjordungstolur/VIN00910.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Samfelag/vinnumarkadur/vinnumarkadsrannsokn/2_arsfjordungstolur/VIN00910.px
table_id: VIN00910
variables:
  time: Ársfjórðungur
  region: Landsvæði
  sex: Kyn
  age: Aldur
  rate: Hlutfall, %
unit: Percent
frequency: quarterly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses total region, males and females, age 16-74, unemployment rate.
```

```yaml
id: statice_residential_property
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Efnahagur/Efnahagur__visitolur__1_vnv__3_greiningarvisitolur/VIS01106.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Efnahagur/VIS01106.px
table_id: VIS01106
variables:
  time: Month
  index: Index
unit: Index
frequency: monthly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses whole country, total.
```

```yaml
id: statice_goods_trade
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Efnahagur/Efnahagur__utanrikisverslun__1_voruvidskipti__01_voruskipti/UTA06002.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Efnahagur/UTA06002.px
table_id: UTA06002
variables:
  time: Month
  trade: Trade
unit: ISK million
frequency: monthly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses goods balance fob-fob.
```

```yaml
id: statice_hotel_overnights
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Atvinnuvegir/Atvinnuvegir__ferdathjonusta__gisting__1_hotelgistiheimili/SAM01102.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Atvinnuvegir/SAM01102.px
table_id: SAM01102
variables:
  citizenship: Ríkisfang
  year: Ár
  region: Landshluti
  month: Mánuður
unit: Overnight stays
frequency: monthly
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses foreigners, total region, monthly values.
```

```yaml
id: statice_public_finance
source: Statistics Iceland
source_url: https://px.hagstofa.is/pxen/pxweb/en/Efnahagur/Efnahagur__fjaropinber__fjarmal_opinber__fjarmal_opinber/THJ05111.px
api_url: https://px.hagstofa.is/pxen/api/v1/en/Efnahagur/THJ05111.px
table_id: THJ05111
variables:
  category: Skipting
  year: Ár
unit: Percent of GDP
frequency: annual
license: CC BY 4.0
attribution: "Source: Statistics Iceland"
verified_at: 2026-05-21
notes: Metadata verified. Query uses financial balance as percent of GDP.
```

## Pending sources

Central Bank of Iceland sources for policy rates, exchange rates, reserves, monetary statistics, and financial-system indicators are documented but not marked production-ready in this MVP. They need stable machine-readable endpoint verification before they can contribute to the score.

```yaml
id: cb_monetary_statistics
source: Central Bank of Iceland
source_url: https://indicators.cb.is/statistics/monetary-statistics/
databank_url: https://databank.is/report/monetary
status: partially_verified
verified_at: 2026-05-21
notes:
  - The Central Bank monetary statistics page says monthly balance-sheet data are available from September 2003 and that detailed data are in Databank.
  - The Databank app exposes report configuration and PowerBI-backed report metadata, including a monetary report with pages for loans, deposits, new credit, and broad money.
  - The new-credit library Excel file has been promoted to production source cb_new_credit.
  - The currently visible Databank endpoints are application endpoints, not a documented statistical API contract. They should not be treated as production source definitions until export semantics, filters, and licensing/attribution behavior are verified.
  - Remaining candidate indicators from this source: outstanding household credit growth, outstanding corporate credit growth, broad money growth.
```

```yaml
id: cb_financial_system_indicators
source: Central Bank of Iceland
source_url: https://indicators.cb.is/
status: pending
verified_at: 2026-05-21
notes:
  - The Central Bank Economic Indicators publication states that underlying chart data can be called up in spreadsheet format.
  - The interactive indicators landing page links Chapter IX, The financial system, to PowerBI.
  - This may be useful for capital, liquidity, or loan-quality indicators, but the chart spreadsheet export path must be confirmed before use.
  - Non-performing loans and bank capital/liquidity indicators remain unavailable for scoring until a stable public download/API path is verified.
```
