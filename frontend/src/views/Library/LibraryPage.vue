<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">Library</h1>
        <p class="text-sm text-slate-400 mt-0.5">Book catalogue, borrowing, and returns.</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        class="px-4 py-2 text-sm font-semibold rounded-lg transition-all"
        :class="activeTab === tab.id ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'">
        {{ tab.label }}
      </button>
    </div>

    <!-- ── Books Tab ───────────────────────────────────────────────── -->
    <template v-if="activeTab === 'books'">
      <div class="bg-white rounded-xl border border-slate-200 p-6 flex flex-wrap gap-3 items-end">
        <div class="flex-1 min-w-48">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search</label>
          <input v-model="bookSearch" type="text" placeholder="Title, author, ISBN…"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
        </div>
        <button @click="showBookModal = true; resetBookForm()"
          class="bg-school-purple text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Add Book
        </button>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div v-if="loadingBooks" class="py-16 flex justify-center">
          <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
        </div>
        <div v-else-if="filteredBooks.length === 0" class="py-12 text-center text-slate-400 text-sm">
          No books found. Add one to get started.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
                <th class="text-left px-6 py-4">Title</th>
                <th class="text-left px-6 py-4">Author</th>
                <th class="text-left px-6 py-4">Category</th>
                <th class="text-center px-6 py-4">Qty</th>
                <th class="text-center px-6 py-4">Available</th>
                <th class="text-left px-6 py-4">Condition</th>
                <th class="text-right px-6 py-4">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="b in filteredBooks" :key="b.id" class="hover:bg-slate-50 transition-colors">
                <td class="px-6 py-4">
                  <p class="font-semibold text-slate-800">{{ b.title }}</p>
                  <p v-if="b.isbn" class="text-xs text-slate-400 font-mono">{{ b.isbn }}</p>
                </td>
                <td class="px-6 py-4 text-slate-600">{{ b.author || '—' }}</td>
                <td class="px-6 py-4 text-slate-500">{{ b.category || '—' }}</td>
                <td class="px-6 py-4 text-center font-medium text-slate-700">{{ b.quantity }}</td>
                <td class="px-6 py-4 text-center">
                  <span class="font-bold" :class="b.available === 0 ? 'text-red-500' : 'text-emerald-600'">
                    {{ b.available }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="px-2 py-0.5 rounded-full text-xs font-bold"
                    :class="b.condition === 'Good' ? 'bg-emerald-50 text-emerald-700' : b.condition === 'Fair' ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-600'">
                    {{ b.condition }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right space-x-3">
                  <button @click="openBorrowForBook(b)" :disabled="b.available === 0"
                    class="text-xs font-semibold text-school-purple hover:text-school-purple-l disabled:opacity-40">Lend</button>
                  <button @click="editBook(b)" class="text-xs font-semibold text-slate-500 hover:text-slate-700">Edit</button>
                  <button @click="deleteBook(b.id)" class="text-xs font-semibold text-red-500 hover:text-red-700">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- ── Borrows Tab ─────────────────────────────────────────────── -->
    <template v-if="activeTab === 'borrows'">
      <div class="bg-white rounded-xl border border-slate-200 p-6 flex flex-wrap gap-3 items-end">
        <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
          <input v-model="activeOnly" type="checkbox" @change="loadBorrows"
            class="rounded border-slate-300 text-school-purple" />
          Show active borrows only
        </label>
        <button @click="showBorrowModal = true; resetBorrowForm()"
          class="ml-auto bg-school-navy text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          New Borrow
        </button>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div v-if="loadingBorrows" class="py-16 flex justify-center">
          <div class="w-8 h-8 border-4 border-slate-200 border-t-school-navy rounded-full animate-spin"></div>
        </div>
        <div v-else-if="borrows.length === 0" class="py-12 text-center text-slate-400 text-sm">No records found.</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
                <th class="text-left px-6 py-4">Book</th>
                <th class="text-left px-6 py-4">Borrower</th>
                <th class="text-center px-6 py-4">Borrowed</th>
                <th class="text-center px-6 py-4">Due</th>
                <th class="text-center px-6 py-4">Returned</th>
                <th class="text-center px-6 py-4">Fine</th>
                <th class="text-right px-6 py-4">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="b in borrows" :key="b.id" class="hover:bg-slate-50 transition-colors"
                :class="b.is_overdue ? 'bg-red-50/30' : ''">
                <td class="px-6 py-4 font-medium text-slate-800">{{ b.book_title }}</td>
                <td class="px-6 py-4">
                  <p class="text-slate-700">{{ b.borrower_name }}</p>
                  <p class="text-xs text-slate-400 capitalize">{{ b.borrower_type }}</p>
                </td>
                <td class="px-6 py-4 text-center text-slate-500 text-xs">{{ fmtDate(b.borrowed_date) }}</td>
                <td class="px-6 py-4 text-center text-xs" :class="b.is_overdue ? 'text-red-600 font-bold' : 'text-slate-500'">
                  {{ fmtDate(b.due_date) }}
                  <span v-if="b.is_overdue" class="block text-xs">OVERDUE</span>
                </td>
                <td class="px-6 py-4 text-center text-xs text-slate-500">{{ b.return_date ? fmtDate(b.return_date) : '—' }}</td>
                <td class="px-6 py-4 text-center text-xs" :class="b.fine_amount > 0 ? 'text-red-600 font-bold' : 'text-slate-400'">
                  {{ b.fine_amount > 0 ? 'KES ' + b.fine_amount : '—' }}
                </td>
                <td class="px-6 py-4 text-right">
                  <button v-if="!b.return_date" @click="returnBook(b.id)"
                    class="text-xs font-semibold text-emerald-600 hover:text-emerald-800">Return</button>
                  <span v-else class="text-xs text-slate-300">Returned</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Add/Edit Book Modal -->
    <div v-if="showBookModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">{{ editingBook ? 'Edit Book' : 'Add Book' }}</h3>
          <button @click="showBookModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Title *</label>
            <input v-model="bookForm.title" type="text" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Author</label>
              <input v-model="bookForm.author" type="text" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">ISBN</label>
              <input v-model="bookForm.isbn" type="text" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Category</label>
              <input v-model="bookForm.category" type="text" placeholder="Textbook, Fiction…" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Quantity</label>
              <input v-model.number="bookForm.quantity" type="number" min="1" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Condition</label>
            <select v-model="bookForm.condition" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
              <option value="Good">Good</option>
              <option value="Fair">Fair</option>
              <option value="Poor">Poor</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showBookModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveBook" :disabled="savingBook"
            class="bg-school-purple text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-school-purple-l disabled:opacity-50">
            {{ savingBook ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

    <!-- New Borrow Modal -->
    <div v-if="showBorrowModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">Record Borrow</h3>
          <button @click="showBorrowModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Book</label>
            <select v-model.number="borrowForm.book_id" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
              <option value="">— Select —</option>
              <option v-for="b in availableBooks" :key="b.id" :value="b.id">{{ b.title }} ({{ b.available }} avail.)</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Borrower Type</label>
              <select v-model="borrowForm.borrower_type" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
                <option value="student">Student</option>
                <option value="staff">Staff</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Due Date</label>
              <input v-model="borrowForm.due_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Borrower Name</label>
            <input v-model="borrowForm.borrower_name" type="text" placeholder="Full name"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showBorrowModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveBorrow" :disabled="savingBorrow"
            class="bg-school-navy text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-school-navy/90 disabled:opacity-50">
            {{ savingBorrow ? 'Saving…' : 'Lend Book' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const tabs = [{ id: 'books', label: 'Catalogue' }, { id: 'borrows', label: 'Borrowing Records' }]
const activeTab = ref('books')

// Books
const books = ref([])
const bookSearch = ref('')
const loadingBooks = ref(false)
const showBookModal = ref(false)
const editingBook = ref(null)
const savingBook = ref(false)
const bookForm = ref({ title: '', author: '', isbn: '', category: '', quantity: 1, condition: 'Good' })

const filteredBooks = computed(() => {
  const q = bookSearch.value.toLowerCase()
  if (!q) return books.value
  return books.value.filter(b =>
    b.title.toLowerCase().includes(q) ||
    (b.author || '').toLowerCase().includes(q) ||
    (b.isbn || '').toLowerCase().includes(q)
  )
})

const availableBooks = computed(() => books.value.filter(b => b.available > 0))

const loadBooks = async () => {
  loadingBooks.value = true
  try { books.value = await apiFetch('/api/library/books') }
  catch { /* silent */ }
  finally { loadingBooks.value = false }
}

const resetBookForm = () => {
  bookForm.value = { title: '', author: '', isbn: '', category: '', quantity: 1, condition: 'Good' }
  editingBook.value = null
}

const editBook = (b) => {
  editingBook.value = b
  bookForm.value = { title: b.title, author: b.author || '', isbn: b.isbn || '', category: b.category || '', quantity: b.quantity, condition: b.condition }
  showBookModal.value = true
}

const saveBook = async () => {
  if (!bookForm.value.title.trim()) return
  savingBook.value = true
  try {
    if (editingBook.value) {
      await apiFetch(`/api/library/books/${editingBook.value.id}`, { method: 'PUT', body: JSON.stringify(bookForm.value) })
    } else {
      await apiFetch('/api/library/books', { method: 'POST', body: JSON.stringify(bookForm.value) })
    }
    showBookModal.value = false
    await loadBooks()
  } catch (e) { toast.error(e?.message || 'Failed to save book.') }
  finally { savingBook.value = false }
}

const deleteBook = async (id) => {
  if (!confirm('Delete this book?')) return
  try {
    await apiFetch(`/api/library/books/${id}`, { method: 'DELETE' })
    await loadBooks()
  } catch (e) { toast.error(e?.message || 'Delete failed.') }
}

// Borrows
const borrows = ref([])
const activeOnly = ref(false)
const loadingBorrows = ref(false)
const showBorrowModal = ref(false)
const savingBorrow = ref(false)
const borrowForm = ref({ book_id: '', borrower_type: 'student', borrower_id: 0, borrower_name: '', due_date: '' })

const loadBorrows = async () => {
  loadingBorrows.value = true
  try {
    borrows.value = await apiFetch(`/api/library/borrows?active_only=${activeOnly.value}`)
  } catch { /* silent */ }
  finally { loadingBorrows.value = false }
}

const resetBorrowForm = () => {
  const due = new Date()
  due.setDate(due.getDate() + 14)
  borrowForm.value = { book_id: '', borrower_type: 'student', borrower_id: 0, borrower_name: '', due_date: due.toISOString().split('T')[0] }
}

const openBorrowForBook = (b) => {
  resetBorrowForm()
  borrowForm.value.book_id = b.id
  showBorrowModal.value = true
}

const saveBorrow = async () => {
  if (!borrowForm.value.book_id || !borrowForm.value.borrower_name || !borrowForm.value.due_date) return
  savingBorrow.value = true
  try {
    await apiFetch('/api/library/borrows', {
      method: 'POST',
      body: JSON.stringify({ ...borrowForm.value, book_id: Number(borrowForm.value.book_id) }),
    })
    showBorrowModal.value = false
    await Promise.all([loadBooks(), loadBorrows()])
  } catch (e) { toast.error(e?.message || 'Failed to record borrow.') }
  finally { savingBorrow.value = false }
}

const returnBook = async (borrowId) => {
  if (!confirm('Mark this book as returned?')) return
  try {
    await apiFetch(`/api/library/borrows/${borrowId}/return`, { method: 'PUT' })
    await Promise.all([loadBooks(), loadBorrows()])
  } catch (e) { toast.error(e?.message || 'Return failed.') }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'

onMounted(async () => {
  await Promise.all([loadBooks(), loadBorrows()])
})
</script>
