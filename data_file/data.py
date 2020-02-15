def init_from_adversarial_batches(self, adv_batches):
    """Initializes work pieces from adversarial batches.

    Args:
      adv_batches: dict with adversarial batches,
        could be obtained as AversarialBatches.data
    """
    for idx, (adv_batch_id, adv_batch_val) in enumerate(iteritems(adv_batches)):
      work_id = ATTACK_WORK_ID_PATTERN.format(idx)
      self.work[work_id] = {
          'claimed_worker_id': None,
          'claimed_worker_start_time': None,
          'is_completed': False,
          'error': None,
          'elapsed_time': None,
          'submission_id': adv_batch_val['submission_id'],
          'shard_id': None,
          'output_adversarial_batch_id': adv_batch_id,
      }