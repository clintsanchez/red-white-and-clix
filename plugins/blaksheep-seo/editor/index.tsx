import { useCallback, useEffect, useState } from 'react'
import {
  Alert,
  Button,
  Card,
  Heading,
  Input,
  Separator,
  Stack,
  Switch,
  Text,
  Textarea,
} from '@instatic/host-ui'
import { useEditorStore } from '@instatic/host-hooks'
import type { EditorPluginApi, EditorPluginModule } from '@core/plugin-sdk'

/**
 * Editor panel — edits the SEO record for whichever page is open.
 *
 * Every `useEditorStore` call selects a PRIMITIVE. Zustand compares selector
 * results with `Object.is`, so a selector returning a fresh object would
 * re-render on every store tick and loop forever.
 */

const RESOURCE = 'page-seo'

/** Google truncates around these; they are guidance, not hard limits. */
const TITLE_LIMIT = 60
const DESCRIPTION_LIMIT = 155

interface StoreLike {
  activePageId: string | null
  site: { pages: Array<Record<string, unknown>> } | null
}

function findPage(state: StoreLike): Record<string, unknown> | null {
  const id = state.activePageId
  if (!id || !state.site) return null
  return state.site.pages.find((page) => page.id === id) ?? null
}

function buildPanel(api: EditorPluginApi) {
  return function SeoPanel() {
    const pageId = useEditorStore((state: StoreLike) => state.activePageId ?? '')
    const pageSlug = useEditorStore((state: StoreLike) => {
      const page = findPage(state)
      return page ? String(page.slug ?? '') : ''
    })
    const pageTitle = useEditorStore((state: StoreLike) => {
      const page = findPage(state)
      return page ? String(page.title ?? '') : ''
    })
    const isTemplate = useEditorStore((state: StoreLike) => {
      const page = findPage(state)
      const template = page?.template as { enabled?: boolean } | undefined
      return template?.enabled === true
    })

    const [recordId, setRecordId] = useState<string | null>(null)
    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [ogImage, setOgImage] = useState('')
    const [noindex, setNoindex] = useState(false)
    const [loading, setLoading] = useState(false)
    const [saving, setSaving] = useState(false)
    const [status, setStatus] = useState<string | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
      if (!pageId || isTemplate) return
      let cancelled = false
      setLoading(true)
      setError(null)
      setStatus(null)
      api.cms.storage
        .collection(RESOURCE)
        .list({ filter: { pageId }, limit: 1 })
        .then((result) => {
          if (cancelled) return
          const record = result.records[0]
          const data = (record?.data ?? {}) as Record<string, unknown>
          setRecordId(record?.id ?? null)
          setTitle(String(data.title ?? ''))
          setDescription(String(data.description ?? ''))
          setOgImage(String(data.ogImage ?? ''))
          setNoindex(data.noindex === true)
        })
        .catch((cause: unknown) => {
          if (!cancelled) setError(`Could not load: ${String(cause)}`)
        })
        .finally(() => {
          if (!cancelled) setLoading(false)
        })
      return () => {
        cancelled = true
      }
    }, [pageId, isTemplate])

    const save = useCallback(async () => {
      if (!pageId) return
      setSaving(true)
      setError(null)
      setStatus(null)
      const data = {
        pageId,
        slug: pageSlug,
        title: title.trim(),
        description: description.trim(),
        ogImage: ogImage.trim(),
        noindex,
      }
      try {
        const collection = api.cms.storage.collection(RESOURCE)
        if (recordId) {
          await collection.update(recordId, data)
        } else {
          const created = await collection.create(data)
          setRecordId(created.id)
        }
        setStatus('Saved. Publish the site to apply it.')
      } catch (cause: unknown) {
        setError(`Could not save: ${String(cause)}`)
      } finally {
        setSaving(false)
      }
    }, [pageId, pageSlug, title, description, ogImage, noindex, recordId])

    if (!pageId) {
      return (
        <Stack direction="column" gap={12}>
          <Text variant="muted">Open a page to edit its search and social metadata.</Text>
        </Stack>
      )
    }

    if (isTemplate) {
      return (
        <Stack direction="column" gap={12}>
          <Alert tone="info" title="Templates are handled by the entry">
            <Text size="sm">
              Pages rendered from this template get their title and description from each
              entry&apos;s own SEO fields in Content. Setting them here would apply the same text
              to every entry, so the panel stays out of the way.
            </Text>
          </Alert>
        </Stack>
      )
    }

    const previewPath = pageSlug === 'index' ? '/' : `/${pageSlug.replace(/^\/+/, '')}`
    const previewTitle = title.trim() || pageTitle
    const previewDescription =
      description.trim() || 'No description yet — the site-wide description will be used.'

    return (
      <Stack direction="column" gap={16}>
        <Stack direction="column" gap={4}>
          <Heading level={3}>{pageTitle}</Heading>
          <Text variant="muted" size="sm">
            {previewPath}
          </Text>
        </Stack>

        {error ? (
          <Alert tone="danger" title="Something went wrong">
            <Text size="sm">{error}</Text>
          </Alert>
        ) : null}

        <Card padding={12} bordered>
          <Stack direction="column" gap={4}>
            <Text variant="muted" size="sm">
              Search preview
            </Text>
            <Text variant="strong">{previewTitle}</Text>
            <Text size="sm">{previewDescription}</Text>
          </Stack>
        </Card>

        <Separator />

        <Input
          label="Meta title"
          value={title}
          placeholder={pageTitle}
          disabled={loading}
          onChange={setTitle}
          description={`${title.length} of about ${TITLE_LIMIT} characters. Leave blank to keep the page title.`}
        />

        <Textarea
          label="Meta description"
          value={description}
          rows={4}
          disabled={loading}
          onChange={setDescription}
          description={`${description.length} of about ${DESCRIPTION_LIMIT} characters. Leave blank to use the site-wide description.`}
        />

        <Input
          label="Social image"
          value={ogImage}
          placeholder="/uploads/rwc/og-default.png"
          disabled={loading}
          onChange={setOgImage}
          description="Shown when the page is shared. Leave blank to use the default social image."
        />

        <Switch
          label="Hide from search engines"
          checked={noindex}
          disabled={loading}
          onChange={setNoindex}
          description="Adds noindex,nofollow. Use for pages that should never appear in results."
        />

        <Stack direction="row" gap={8} align="center">
          <Button variant="primary" disabled={loading || saving} onClick={save}>
            {saving ? 'Saving…' : 'Save'}
          </Button>
          {status ? (
            <Text variant="muted" size="sm">
              {status}
            </Text>
          ) : null}
        </Stack>

        <Text variant="muted" size="sm">
          Counters are guidance, not limits. Longer text still publishes — search engines simply
          trim what they show.
        </Text>
      </Stack>
    )
  }
}

export default {
  activate(api: EditorPluginApi) {
    api.editor.panels.register({
      id: 'blaksheep.seo.panel',
      label: 'SEO',
      iconName: 'search-solid',
      accent: 'sky',
      component: buildPanel(api),
    })
  },
} satisfies EditorPluginModule
