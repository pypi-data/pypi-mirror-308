import torch


class ContrastiveLoss(torch.nn.Module):
    """
    Contrastive loss
    Adapted from: (OnlineContrastiveLoss)
        https://github.com/adambielski/siamese-triplet/blob/master/losses.py
    Based on: http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
    """

    def __init__(self, margin):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, anchors, negatives, positives):
        anchors = anchors / anchors.norm(dim=-1, keepdim=True)
        negatives = negatives / negatives.norm(dim=-1, keepdim=True)
        positives = positives / positives.norm(dim=-1, keepdim=True)

        positive_loss = (anchors - positives).pow(2).sum(1)
        negative_loss = torch.nn.functional.relu(
            self.margin - (anchors - negatives).pow(2).sum(1).sqrt()).pow(2)

        loss = 0.5 * torch.cat([positive_loss, negative_loss], dim=0)

        return loss.mean()
