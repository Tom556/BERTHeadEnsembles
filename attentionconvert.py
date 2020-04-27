from udapi.core.block import Block


class AttentionConvert(Block):
	"""This block takes all prepositions (upos=ADP) and rehangs them above their parent."""

	@staticmethod
	def __rehang_children(origparent, new_parent, udeprels_to_move):
		for node in [n for n in origparent.children if n.udeprel in udeprels_to_move]:
			node.parent = new_parent

	def process_tree(self, root):
		
		# rearange copulas
		# NOTE: 5
		udeprels_to_move = {'nsubj', 'aux', 'csubj', 'ccomp', 'xcomp', 'advcl',
		                    'acl', 'parataxis', 'expl', 'punct', 'obj'}
		for node in root.descendants():
			if node.deprel == 'cop':
				origparent = node.parent
				node.parent = origparent.parent
				origparent.parent = node
				
				node.deprel = origparent.deprel
				origparent.deprel = 'dep'
				
				self.__rehang_children(origparent, node, udeprels_to_move)
		
		# change expletives to nominal subjects
		# NOTE: 7
		for node in root.descendants():
			if node.deprel == 'expl' and node.precedes(node.parent):
				for sibling in node.parent.children:
					if sibling.udeprel == 'nsubj':
						sibling.deprel = 'obj'
				node.deprel = 'nsubj'
				

		for node in root.descendants():
			if node.udeprel == 'conj':
				conj_parent = node.parent
				# if conj_parent.udeprel == 'root' or conj_parent.parent.udeprel == 'root':
				# 	pass
				# else:
				for right_brother in [ch for ch in node.parent.children if ch.ord > node.ord]:
					if right_brother.deprel == 'conj':
						right_brother.parent = node
					elif right_brother.deprel == 'cc' or (right_brother.deprel == 'punct' and right_brother.lemma in [',', ';']):
						right_brother.parent = node
